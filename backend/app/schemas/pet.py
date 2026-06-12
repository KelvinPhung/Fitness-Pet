"""
Pydantic schemas for pet endpoints
"""
from pydantic import BaseModel, Field
from typing import Optional


class PetCreateRequest(BaseModel):
    """Schema for pet creation request"""
    
    name: str = Field(..., min_length=1, max_length=100, description="Pet name (1-100 characters)")
    species: str = Field(..., description="Pet species: dog, cat, rabbit, bird, or dragon")


class PetFocusResponse(BaseModel):
    """Schema for pet focus information"""
    
    id: int
    pet_id: int
    strength_focus: int
    endurance_focus: int
    speed_focus: int
    
    class Config:
        from_attributes = True


class PetResponse(BaseModel):
    """Schema for pet response"""
    
    id: int
    user_id: int
    name: str
    species: str
    level: int
    experience: int
    evolution_stage: int
    strength_xp: int
    endurance_xp: int
    speed_xp: int
    created_at: str
    updated_at: str
    pet_focus: Optional[PetFocusResponse] = None
    
    class Config:
        from_attributes = True


class PetListResponse(BaseModel):
    """Schema for list of pets"""
    
    pets: list[PetResponse]
    total: int


class PetUpdateRequest(BaseModel):
    """Schema for updating pet name"""
    
    name: str = Field(..., min_length=1, max_length=100, description="New pet name")