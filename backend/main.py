from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from typing import List, Optional
import os
from datetime import datetime, timedelta
import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# Initialize FastAPI app
app = FastAPI(
    title="Sports Council Recruitment Task API",
    description="API for the Sports Council Tournament Registration System",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in development
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Database connection
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.environ.get("MONGO_DATABASE", "sports_council_recruitment")

@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(MONGO_URI)
    app.mongodb = app.mongodb_client[MONGO_DB]
    
    # Create initial admin user if it doesn't exist
    user_collection = app.mongodb.users
    if await user_collection.count_documents({"username": "admin"}) == 0:
        await user_collection.insert_one({
            "username": "admin",
            "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # "password"
            "is_admin": True
        })

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()

# JWT Configuration
SECRET_KEY = os.environ.get("JWT_SECRET", "your_secret_key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Basic Models
class TokenData(BaseModel):
    username: str
    is_admin: bool

class User(BaseModel):
    username: str
    is_admin: bool = False

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class Tournament(BaseModel):
    id: Optional[str] = None
    name: str
    sport: str
    start_date: str
    end_date: str
    registration_deadline: str
    description: Optional[str] = None
    max_teams: int
    current_teams: Optional[int] = 0

class Registration(BaseModel):
    id: Optional[str] = None
    tournament_id: str
    team_name: str
    captain_name: str
    captain_email: str
    player_names: List[str]
    registration_date: Optional[str] = None

# Helper Functions
async def get_user(db, username: str):
    user_dict = await db.users.find_one({"username": username})
    if user_dict:
        return UserInDB(**user_dict)
    return None

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        is_admin: bool = payload.get("is_admin", False)
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username, is_admin=is_admin)
    except jwt.PyJWTError:
        raise credentials_exception
    
    user = await get_user(app.mongodb, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_admin_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can access this resource",
        )
    return current_user

# Routes
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    import bcrypt
    
    user = await get_user(app.mongodb, form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify password
    is_password_correct = bcrypt.checkpw(
        form_data.password.encode('utf-8'), 
        user.hashed_password.encode('utf-8')
    )
    
    if not is_password_correct:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "is_admin": user.is_admin},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/user/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@app.get("/api/tournaments")
async def get_tournaments():
    tournaments = []
    cursor = app.mongodb.tournaments.find({})
    async for document in cursor:
        document["id"] = str(document.pop("_id"))
        tournaments.append(document)
    return tournaments

@app.get("/api/tournaments/{tournament_id}")
async def get_tournament(tournament_id: str):
    from bson import ObjectId
    
    tournament = await app.mongodb.tournaments.find_one({"_id": ObjectId(tournament_id)})
    if tournament:
        tournament["id"] = str(tournament.pop("_id"))
        return tournament
    
    raise HTTPException(status_code=404, detail=f"Tournament {tournament_id} not found")

@app.post("/api/tournaments", status_code=status.HTTP_201_CREATED)
async def create_tournament(tournament: Tournament, current_user: User = Depends(get_admin_user)):
    new_tournament = tournament.dict()
    new_tournament["current_teams"] = 0
    
    result = await app.mongodb.tournaments.insert_one(new_tournament)
    created_tournament = await app.mongodb.tournaments.find_one({"_id": result.inserted_id})
    created_tournament["id"] = str(created_tournament.pop("_id"))
    
    return created_tournament

@app.put("/api/tournaments/{tournament_id}")
async def update_tournament(tournament_id: str, tournament: Tournament, current_user: User = Depends(get_admin_user)):
    from bson import ObjectId
    
    await app.mongodb.tournaments.update_one(
        {"_id": ObjectId(tournament_id)},
        {"$set": tournament.dict(exclude={"id"})}
    )
    
    updated_tournament = await app.mongodb.tournaments.find_one({"_id": ObjectId(tournament_id)})
    if updated_tournament:
        updated_tournament["id"] = str(updated_tournament.pop("_id"))
        return updated_tournament
        
    raise HTTPException(status_code=404, detail=f"Tournament {tournament_id} not found")

@app.delete("/api/tournaments/{tournament_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tournament(tournament_id: str, current_user: User = Depends(get_admin_user)):
    from bson import ObjectId
    
    delete_result = await app.mongodb.tournaments.delete_one({"_id": ObjectId(tournament_id)})
    
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"Tournament {tournament_id} not found")
    
    return {"message": "Tournament deleted successfully"}

@app.post("/api/registrations", status_code=status.HTTP_201_CREATED)
async def create_registration(registration: Registration):
    from bson import ObjectId
    import time
    
    # Check if tournament exists and has space
    tournament = await app.mongodb.tournaments.find_one({"_id": ObjectId(registration.tournament_id)})
    if not tournament:
        raise HTTPException(status_code=404, detail=f"Tournament {registration.tournament_id} not found")
    
    if tournament["current_teams"] >= tournament["max_teams"]:
        raise HTTPException(status_code=400, detail="Tournament registration is full")
    
    # Check if registration deadline has passed
    deadline = datetime.strptime(tournament["registration_deadline"], "%Y-%m-%d")
    if datetime.now() > deadline:
        raise HTTPException(status_code=400, detail="Registration deadline has passed")
    
    # Prepare registration data
    new_registration = registration.dict()
    new_registration["registration_date"] = datetime.now().strftime("%Y-%m-%d")
    
    # Insert registration
    result = await app.mongodb.registrations.insert_one(new_registration)
    
    # Update tournament team count
    await app.mongodb.tournaments.update_one(
        {"_id": ObjectId(registration.tournament_id)},
        {"$inc": {"current_teams": 1}}
    )
    
    created_registration = await app.mongodb.registrations.find_one({"_id": result.inserted_id})
    created_registration["id"] = str(created_registration.pop("_id"))
    
    return created_registration

@app.get("/api/registrations/{tournament_id}")
async def get_registrations_by_tournament(tournament_id: str, current_user: User = Depends(get_current_user)):
    from bson import ObjectId
    
    # Verify tournament exists
    tournament = await app.mongodb.tournaments.find_one({"_id": ObjectId(tournament_id)})
    if not tournament:
        raise HTTPException(status_code=404, detail=f"Tournament {tournament_id} not found")
    
    registrations = []
    cursor = app.mongodb.registrations.find({"tournament_id": tournament_id})
    async for document in cursor:
        document["id"] = str(document.pop("_id"))
        registrations.append(document)
    
    return registrations

@app.get("/")
async def root():
    return {"message": "Welcome to the Sports Council Tournament API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)