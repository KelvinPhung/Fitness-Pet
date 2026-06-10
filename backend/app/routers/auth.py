"""
Authentication endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.auth import (
    UserRegisterRequest,
    UserLoginRequest,
    UserResponse,
    TokenResponse,
    TokenData
)
from app.services.user import UserService
from app.services.security import TokenService, PasswordService

router = APIRouter(prefix="/api/auth", tags=["authentication"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(
    user_data: UserRegisterRequest,
    db: Session = Depends(get_db)
):
    """
    Register a new user
    
    **Request Body:**
    - `username`: Username (3-50 characters, alphanumeric and underscores only)
    - `email`: Valid email address
    - `password`: Password (minimum 8 characters)
    
    **Response:**
    - `access_token`: JWT token for authentication
    - `token_type`: Token type (always "bearer")
    - `user`: User information
    
    **Errors:**
    - `400`: Username or email already exists
    - `422`: Invalid input data
    """
    
    # Check if user already exists
    if UserService.user_exists(db, username=user_data.username, email=user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered"
        )
    
    # Create new user
    user = UserService.create_user(db, user_data)
    
    # Generate access token
    access_token = TokenService.create_access_token(
        user_id=user.id,
        username=user.username
    )
    
    return TokenResponse(
        access_token=access_token,
        user=UserResponse.model_validate(user)
    )


@router.post("/login", response_model=TokenResponse)
def login(
    credentials: UserLoginRequest,
    db: Session = Depends(get_db)
):
    """
    Login with username/email and password
    
    **Request Body:**
    - `username`: Username or email
    - `password`: Password
    
    **Response:**
    - `access_token`: JWT token for authentication
    - `token_type`: Token type (always "bearer")
    - `user`: User information
    
    **Errors:**
    - `401`: Invalid credentials
    """
    
    # Authenticate user
    user = UserService.authenticate_user(db, credentials.username, credentials.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username/email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Generate access token
    access_token = TokenService.create_access_token(
        user_id=user.id,
        username=user.username
    )
    
    return TokenResponse(
        access_token=access_token,
        user=UserResponse.model_validate(user)
    )


def get_current_user(
    token: str = None,
    db: Session = Depends(get_db)
) -> TokenData:
    """
    Dependency to extract and verify current user from JWT token
    
    Args:
        token: JWT token from Authorization header
        db: Database session
        
    Returns:
        TokenData with user_id and username
        
    Raises:
        HTTPException: If token is invalid or expired
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Remove "Bearer " prefix if present
    if token.startswith("Bearer "):
        token = token[7:]
    
    token_data = TokenService.verify_token(token)
    
    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return token_data


@router.get("/me", response_model=UserResponse)
def get_current_user_info(
    current_user: TokenData = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current authenticated user information
    
    **Headers:**
    - `Authorization: Bearer <token>`
    
    **Response:**
    - User information
    
    **Errors:**
    - `401`: Invalid or missing token
    """
    
    # Get user from database
    user = UserService.get_user_by_id(db, current_user.user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserResponse.model_validate(user)
