"""
User service for database operations
"""
from typing import Optional

from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.auth import UserRegisterRequest
from app.services.security import PasswordService


class UserService:
    """Service for user-related database operations"""
    
    @staticmethod
    def create_user(db: Session, user_data: UserRegisterRequest) -> User:
        """
        Create a new user in the database
        
        Args:
            db: Database session
            user_data: User registration data
            
        Returns:
            Created User object
        """
        hashed_password = PasswordService.hash_password(user_data.password)
        
        user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        return user
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        """
        Get user by ID
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            User object or None if not found
        """
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> Optional[User]:
        """
        Get user by username
        
        Args:
            db: Database session
            username: Username
            
        Returns:
            User object or None if not found
        """
        return db.query(User).filter(User.username == username).first()
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """
        Get user by email
        
        Args:
            db: Database session
            email: Email address
            
        Returns:
            User object or None if not found
        """
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def user_exists(db: Session, username: str = None, email: str = None) -> bool:
        """
        Check if user exists by username or email
        
        Args:
            db: Database session
            username: Username to check (optional)
            email: Email to check (optional)
            
        Returns:
            True if user exists, False otherwise
        """
        if username:
            if db.query(User).filter(User.username == username).first():
                return True
        
        if email:
            if db.query(User).filter(User.email == email).first():
                return True
        
        return False
    
    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
        """
        Authenticate a user by username/email and password
        
        Args:
            db: Database session
            username: Username or email
            password: Plain text password
            
        Returns:
            User object if authentication successful, None otherwise
        """
        # Try to find user by username or email
        user = db.query(User).filter(
            (User.username == username) | (User.email == username)
        ).first()
        
        if not user or not user.is_active:
            return None
        
        # Verify password
        if not PasswordService.verify_password(password, user.hashed_password):
            return None
        
        return user