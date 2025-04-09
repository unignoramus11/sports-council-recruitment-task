"""
Tournament models for the Sports Council application.
"""

from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class TournamentFormat(str, Enum):
    KNOCKOUT = "knockout"
    LEAGUE = "league"
    ROUND_ROBIN = "round_robin"
    CUSTOM = "custom"

class TournamentStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    REGISTRATION_OPEN = "registration_open"
    REGISTRATION_CLOSED = "registration_closed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

# TODO: Implement Tournament models

class TournamentBase(BaseModel):
    """Base Tournament model with common attributes"""
    # Implement the base tournament model with required fields
    pass

class TournamentCreate(TournamentBase):
    """Tournament creation model"""
    # Extend the base model with fields needed for creation
    pass

class TournamentUpdate(BaseModel):
    """Tournament update model with optional fields"""
    # Implement update model with all fields optional
    pass

class TournamentInDB(TournamentBase):
    """Tournament model as stored in database"""
    id: str = Field(..., alias="_id")
    
    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True