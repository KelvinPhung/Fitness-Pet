"""
Pet management endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session

from app.database import get_db
from app.routers.auth import get_current_user
from app.schemas.auth import TokenData
from app.schemas.pet import (
    PetCreateRequest,
    PetResponse,
    PetListResponse,
    PetUpdateRequest
)
from app.services.pet import PetService

router = APIRouter(prefix="/api/pets", tags=["pets"])


@router.post("/create", response_model=PetResponse, status_code=status.HTTP_201_CREATED)
def create_pet(
    pet_data: PetCreateRequest,
    current_user: TokenData = Depends(get_current_user),
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """
    Create a new pet for the current user
    
    **Request Body:**
    - `name`: Pet name (1-100 characters)
    - `species`: Pet species (dog, cat, rabbit, bird, dragon)
    
    **Response:**
    - New pet object with default focus (50% strength, 30% endurance, 20% speed)
    
    **Errors:**
    - `400`: Invalid species
    - `401`: Invalid or missing token
    """
    
    try:
        pet = PetService.create_pet(
            db=db,
            user_id=current_user.user_id,
            name=pet_data.name,
            species=pet_data.species
        )
        return PetResponse.model_validate(pet)
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("", response_model=PetListResponse)
def get_all_pets(
    current_user: TokenData = Depends(get_current_user),
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """
    Get all pets for the current user
    
    **Headers:**
    - `Authorization: Bearer <token>`
    
    **Response:**
    - List of pets with count
    
    **Errors:**
    - `401`: Invalid or missing token
    """
    
    pets = PetService.get_user_pets(db, current_user.user_id)
    
    return PetListResponse(
        pets=[PetResponse.model_validate(pet) for pet in pets],
        total=len(pets)
    )


@router.get("/{pet_id}", response_model=PetResponse)
def get_pet(
    pet_id: int,
    current_user: TokenData = Depends(get_current_user),
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """
    Get a specific pet by ID (must own the pet)
    
    **Path Parameters:**
    - `pet_id`: Pet ID
    
    **Headers:**
    - `Authorization: Bearer <token>`
    
    **Response:**
    - Pet object
    
    **Errors:**
    - `401`: Invalid or missing token
    - `403`: Pet belongs to another user
    - `404`: Pet not found
    """
    
    pet = PetService.get_pet_by_id(db, pet_id)
    
    if not pet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pet not found"
        )
    
    # Verify ownership
    if pet.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this pet"
        )
    
    return PetResponse.model_validate(pet)


@router.put("/{pet_id}", response_model=PetResponse)
def update_pet(
    pet_id: int,
    pet_data: PetUpdateRequest,
    current_user: TokenData = Depends(get_current_user),
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """
    Update pet name (currently only name can be updated)
    
    **Path Parameters:**
    - `pet_id`: Pet ID
    
    **Request Body:**
    - `name`: New pet name (1-100 characters)
    
    **Headers:**
    - `Authorization: Bearer <token>`
    
    **Response:**
    - Updated pet object
    
    **Errors:**
    - `401`: Invalid or missing token
    - `403`: Pet belongs to another user
    - `404`: Pet not found
    """
    
    pet = PetService.get_pet_by_id(db, pet_id)
    
    if not pet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pet not found"
        )
    
    # Verify ownership
    if pet.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update this pet"
        )
    
    # Update name
    pet.name = pet_data.name
    db.commit()
    db.refresh(pet)
    
    return PetResponse.model_validate(pet)


@router.delete("/{pet_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pet(
    pet_id: int,
    current_user: TokenData = Depends(get_current_user),
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """
    Delete a pet (cascades to activities and achievements)
    
    **Path Parameters:**
    - `pet_id`: Pet ID
    
    **Headers:**
    - `Authorization: Bearer <token>`
    
    **Response:**
    - 204 No Content on success
    
    **Errors:**
    - `401`: Invalid or missing token
    - `403`: Pet belongs to another user
    - `404`: Pet not found
    """
    
    pet = PetService.get_pet_by_id(db, pet_id)
    
    if not pet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pet not found"
        )
    
    # Verify ownership
    if pet.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this pet"
        )
    
    PetService.delete_pet(db, pet_id)