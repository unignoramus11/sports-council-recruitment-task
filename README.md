# Sports Council Tech Team - Recruitment Task

## Overview

This recruitment task is designed to thoroughly assess your technical expertise with the Sports Council Website's technology stack at IIIT Hyderabad. You'll be building a comprehensive sports event management system that showcases your proficiency in:

- **Frontend**: Svelte/SvelteKit with Flowbite-Svelte components
- **Backend**: Python FastAPI
- **Database**: MongoDB
- **Deployment**: Docker
- **Testing**: Jest (Frontend), Pytest (Backend)
- **Authentication**: JWT-based with role permissions

## Challenge Timeline: 2 Months

This task is intentionally extensive to evaluate your ability to handle complex feature implementation, architectural decisions, performance optimization, and production-ready code-skills we value in our development team. Do note whatever you make should look great on all screen sizes.

## The Challenge: Advanced Tournament Management System

### What's Provided

- Basic project structure with Docker setup
- Minimal skeleton code for frontend and backend
- MongoDB connection setup
- Simple authentication flow

### What You Need to Build (Core Requirements)

1. **Tournament Management**

   - Create a complete tournament lifecycle management system
   - Implement a tournament bracket/elimination system with match scheduling
   - Build a results tracking system with leaderboards
   - Add support for different tournament formats (leagues, knockouts, round-robin)
   - (Bonus) Implement a real-time match update system using WebSockets

2. **Advanced Registration System**

   - Create sport-specific registration forms with dynamic fields
   - (Bonus) Integrate these forms with CAS (Central Authentication Service) to ease the process for users
   - Implement team management with player profiles and statistics
   - Add validation for team eligibility (minimum/maximum players, etc.)
   - Build a waitlist system for tournaments that are full

3. **Venue Management**

   - Create a system to manage sports venues and resources
   - Implement booking/scheduling to prevent conflicts
   - Add venue availability visualization through a calendar interface

4. **User System**

   - Implement multi-role user system (admin, organizer, captain, player)
   - Create a permissions system with fine-grained access control
   - Add user profiles with sports participation history
   - (Bonus) Implement email notifications for important events

5. **Admin Dashboard**

   - Build comprehensive analytics for tournament participation
   - Create tournament management workflows with approval processes
   - Implement content management for tournament rules and announcements
   - Add administrative controls for user management
   - Implement a logging system for tracking changes and actions with audit trails

### Technical Requirements

#### Frontend

- Build a responsive, accessible UI with Flowbite-Svelte components
- Implement advanced state management patterns using Svelte stores
- Create lazy-loaded routes for performance optimization
- Build reusable, well-documented component library
- Implement client-side form validation with proper error handling
- Add dark/light theme support
- Write unit and integration tests for critical components
- **Provide comprehensive user feedback** through toast notifications for all user actions
- **Design intuitive user flows** that are clear for first-time users
- **Implement thoughtful UI states** (loading, error, success, empty) for all interactions

#### Backend

- Implement a well-structured, modular API with proper separation of concerns
- Create comprehensive input validation and error handling
- Implement database transactions for data integrity
- Add rate limiting and security best practices
- Implement caching strategies for performance
- Create a comprehensive test suite with pytest
- Document all API endpoints with OpenAPI/Swagger

#### Database

- Design efficient and normalized MongoDB schemas
- Implement proper indexing strategies for query optimization
- Create data validation at the database level
- Implement data aggregation pipelines for analytics
- Add data migration strategies

#### DevOps

- Extend Docker setup for development and production environments
- (Bonus) Add CI/CD pipeline configuration
- Implement logging and monitoring strategies
- Create backup and restore procedures

## Getting Started

We've provided you with a minimal project structure to get started. You'll need to extend and enhance this foundation.

1. Start the development environment:

```bash
docker-compose up
```

2. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Project Structure

The repository contains a basic structure that you'll need to extend:

```
recruitment-task/
├── frontend/               # SvelteKit application (extend this)
├── backend/                # FastAPI application (extend this)
├── nginx/                  # Nginx configuration (may need updates)
├── docker-compose.yml      # Docker compose setup (extend as needed)
└── README.md               # Project documentation
```

## Milestones (Suggested Timeline)

### Week 1: Foundation and Core Features

- Set up enhanced project structure
- Implement basic models and database schemas
- Create core API endpoints
- Set up authentication and user management
- Build base UI components and layouts

### Week 2: Tournament and Registration Systems

- Develop tournament management features
- Implement advanced registration system
- Create team management functionality
- Build tournament bracket visualization

### Week 3: Advanced Features

- Implement venue management system
- Create reporting and analytics dashboards
- Build notification system
- Add advanced filtering and search capabilities

### Week 4: Refinement and Quality Assurance

- Write comprehensive tests
- Optimize performance
- Enhance UI/UX
- Add documentation
- Final polishing

## Evaluation Criteria

Your solution will be evaluated based on:

1. **Technical Excellence**

   - Code quality and organization
   - Architecture and design patterns
   - Performance optimization
   - Security implementation

2. **Completeness and Functionality**

   - Feature implementation
   - Error handling and edge cases
   - Usability of the solution

3. **User Experience (UX)**

   - **We strongly consider UX in our evaluation**
   - Identify what aspects of usability metrics are lacking in the current website
   - Provide appropriate feedback for every user action (toast notifications, etc.)
   - Create intuitive workflows that are clear to first-time users
   - Design consistent and accessible interfaces
   - Implement responsive design that works well across all devices
   - These principles apply to all the interfaces, including create and edit pages

4. **Best Practices**

   - Testing approach
   - Documentation quality
   - Adherence to coding standards
   - Git workflow and commit quality (excuse the big bang commit in the template repo :p)

5. **Innovation and Problem-Solving**
   - Creative solutions to complex problems
   - Extra features and improvements
   - User experience considerations

## Submission Guidelines

1. Make regular, meaningful commits showing your progress:
   - Use clear commit messages
   - Follow a consistent branching strategy (feature branches, etc.)
2. Before submitting:
   - Push all your changes
   - Ensure everything runs in your Docker setup
   - Add a final README inside your repo documenting:
     - Architecture and design decisions
     - Features implemented
     - Installation and setup instructions
     - Known limitations and future improvements
     - Testing strategy
3. When you're ready, fill the submission form to notify us:
   - [Submission Form](https://forms.office.com/r/ziUueqhyq0)

## Notes

- This is an intentionally challenging task. We do NOT expect 100% completion of all features.
- Focus on quality over quantity: well-implemented core features are better than many incomplete ones.
- Document any compromises and decisions you made due to time constraints.
- Feel free to use additional libraries that might help you, but document your choices.

If you have questions or need clarification, please open an issue in the repository.

Good luck! We're looking forward to seeing your approach to this challenge.
