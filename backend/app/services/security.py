"""
Security utilities for password hashing and JWT token management
"""
from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import ValidationError

from app.config import settings
from app.schemas.auth import TokenData

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswordService:
    """Service for password hashing and verification"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt"""
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a plain password against a hashed password"""
        return pwd_context.verify(plain_password, hashed_password)


class TokenService:
    """Service for JWT token generation and validation"""
    
    @staticmethod
    def create_access_token(
        user_id: int,
        username: str,
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Create a JWT access token
        
        Args:
            user_id: User ID to encode in token
            username: Username to encode in token
            expires_delta: Custom expiration time delta
            
        Returns:
            Encoded JWT token
        """
        if expires_delta is None:
            expires_delta = timedelta(minutes=settings.access_token_expire_minutes)
        
        expire = datetime.utcnow() + expires_delta
        payload = {
            "user_id": user_id,
            "username": username,
            "exp": expire
        }
        
        encoded_jwt = jwt.encode(
            payload,
            settings.secret_key,
            algorithm=settings.algorithm
        )
        
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str) -> Optional[TokenData]:
        """
        Verify and decode a JWT token
        
        Args:
            token: JWT token to verify
            
        Returns:
            TokenData if valid, None if invalid
        """
        try:
            payload = jwt.decode(
                token,
                settings.secret_key,
                algorithms=[settings.algorithm]
            )
            user_id: int = payload.get("user_id")
            username: str = payload.get("username")
            
            if user_id is None or username is None:
                return None
            
            return TokenData(user_id=user_id, username=username)
        
        except (JWTError, ValidationError):
            return None