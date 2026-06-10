"""
Pydantic schemas for authentication endpoints
"""
from pydantic import BaseModel, EmailStr, Field, field_validator


class UserRegisterRequest(BaseModel):
    """Schema for user registration request"""
    
    username: str = Field(..., min_length=3, max_length=50, description="Username (3-50 characters)")
    email: EmailStr = Field(..., description="Valid email address")
    password: str = Field(..., min_length=8, description="Password (minimum 8 characters)")
    
    @field_validator("username")
    @classmethod
    def username_alphanumeric(cls, v: str) -> str:
        """Validate username contains only alphanumeric and underscores"""
        if not v.replace("_", "").isalnum():
            raise ValueError("Username must contain only alphanumeric characters and underscores")
        return v


class UserLoginRequest(BaseModel):
    """Schema for user login request"""
    
    username: str = Field(..., description="Username or email")
    password: str = Field(..., description="Password")


class UserResponse(BaseModel):
    """Schema for user response (public data)"""
    
    id: int
    username: str
    email: str
    is_active: bool
    created_at: str
    
    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """Schema for authentication token response"""
    
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class TokenData(BaseModel):
    """Schema for JWT token payload"""
    
    user_id: int
    username: str