"""
Application initialization and startup
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.config import settings

# Import routers (will be added in later phases)
# from app.routers import auth, users, pets, activities, friends

# Create database tables
Base.metadata.create_all(bind=engine)


def create_app():
    """Create and configure the FastAPI application"""
    
    app = FastAPI(
        title="Fitness Pet Evolution API",
        description="A fitness gamification platform where users raise a virtual pet through real-world exercise",
        version="0.1.0",
        debug=settings.debug
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Update this for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers (will be added in later phases)
    # app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
    # app.include_router(users.router, prefix="/api/users", tags=["users"])
    # app.include_router(pets.router, prefix="/api/pets", tags=["pets"])
    # app.include_router(activities.router, prefix="/api/activities", tags=["activities"])
    # app.include_router(friends.router, prefix="/api/friends", tags=["friends"])
    
    @app.get("/")
    def read_root():
        """Health check endpoint"""
        return {
            "message": "Fitness Pet Evolution API",
            "status": "running",
            "version": "0.1.0"
        }
    
    @app.get("/health")
    def health_check():
        """Health check endpoint for monitoring"""
        return {"status": "healthy"}
    
    return app


app = create_app()