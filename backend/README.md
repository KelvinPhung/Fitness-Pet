# Fitness Pet Evolution - Backend Setup

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── config.py               # Configuration settings
│   ├── database.py             # SQLAlchemy setup
│   ├── models/                 # Database models (ORM)
│   │   └── __init__.py
│   ├── routers/                # API endpoints
│   │   └── __init__.py
│   ├── schemas/                # Pydantic schemas (validation)
│   │   └── __init__.py
│   └── services/               # Business logic
│       └── __init__.py
├── run.py                      # Development server entry point
├── requirements.txt            # Python dependencies
├── .env.example                # Environment configuration template
└── .gitignore                  # Git ignore rules
```

## Getting Started

### 1. Setup Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your configuration
```

### 3. Run Development Server

```bash
python run.py
```

The API will be available at `http://localhost:8000`

#### Interactive API Documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Phase 1 - Backend Foundation ✅

**Completed:**
- ✅ FastAPI application setup
- ✅ SQLAlchemy with SQLite configuration
- ✅ Project folder structure
- ✅ Configuration management
- ✅ Database session management
- ✅ CORS middleware
- ✅ Health check endpoints

**Next Phase:** Authentication (Phase 2)

## Architecture Overview

### Configuration
- `config.py`: Centralized settings management using Pydantic

### Database
- `database.py`: SQLAlchemy engine, session factory, and dependency injection
- Uses SQLite for development (easily switchable to PostgreSQL)

### Application
- `main.py`: FastAPI app initialization with middleware and route registration
- `run.py`: Development server entry point

### Modular Structure
- `models/`: SQLAlchemy ORM models
- `routers/`: FastAPI route handlers organized by domain
- `schemas/`: Pydantic models for request/response validation
- `services/`: Reusable business logic layer

## Database

The application uses **SQLite** for development and can be easily switched to PostgreSQL for production.

Database file will be created automatically: `fitness_pet.db`

## Next Steps

1. ✅ Backend Foundation (DONE)
2. 🔄 Phase 2: Authentication System
   - User registration
   - Login with JWT tokens
   - Protected routes
3. Phase 3: Database Models
4. Phase 4: Pet Creation System
5. Phase 5: Focus System
... and so on