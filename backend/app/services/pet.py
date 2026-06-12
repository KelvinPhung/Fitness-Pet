"""
Pet service for creating and managing pets
"""
from typing import Optional

from sqlalchemy.orm import Session

from app.models.pet import Pet, PetSpecies
from app.models.pet_focus import PetFocus


class PetService:
    """Service for pet-related operations"""
    
    @staticmethod
    def create_pet(
        db: Session,
        user_id: int,
        name: str,
        species: str
    ) -> Pet:
        """
        Create a new pet for a user
        
        Args:
            db: Database session
            user_id: Owner user ID
            name: Pet name
            species: Pet species (dog, cat, rabbit, bird, dragon)
            
        Returns:
            Created Pet object
            
        Raises:
            ValueError: If species is invalid
        """
        
        # Validate species
        valid_species = [s.value for s in PetSpecies]
        if species not in valid_species:
            raise ValueError(f"Invalid species. Must be one of: {', '.join(valid_species)}")
        
        # Create pet
        pet = Pet(
            user_id=user_id,
            name=name,
            species=species,
            level=1,
            experience=0,
            evolution_stage=1,
            strength_xp=0,
            endurance_xp=0,
            speed_xp=0
        )
        
        db.add(pet)
        db.flush()  # Flush to get the pet ID without committing
        
        # Create default focus (50% strength, 30% endurance, 20% speed)
        pet_focus = PetFocus(
            pet_id=pet.id,
            strength_focus=50,
            endurance_focus=30,
            speed_focus=20
        )
        
        db.add(pet_focus)
        db.commit()
        db.refresh(pet)
        
        return pet
    
    @staticmethod
    def get_pet_by_id(db: Session, pet_id: int) -> Optional[Pet]:
        """
        Get pet by ID
        
        Args:
            db: Database session
            pet_id: Pet ID
            
        Returns:
            Pet object or None if not found
        """
        return db.query(Pet).filter(Pet.id == pet_id).first()
    
    @staticmethod
    def get_user_pets(db: Session, user_id: int) -> list[Pet]:
        """
        Get all pets for a user
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            List of Pet objects
        """
        return db.query(Pet).filter(Pet.user_id == user_id).all()
    
    @staticmethod
    def pet_belongs_to_user(db: Session, pet_id: int, user_id: int) -> bool:
        """
        Check if a pet belongs to a user
        
        Args:
            db: Database session
            pet_id: Pet ID
            user_id: User ID
            
        Returns:
            True if pet belongs to user, False otherwise
        """
        pet = db.query(Pet).filter(Pet.id == pet_id, Pet.user_id == user_id).first()
        return pet is not None
    
    @staticmethod
    def delete_pet(db: Session, pet_id: int) -> bool:
        """
        Delete a pet (cascades to activities, achievements, focus)
        
        Args:
            db: Database session
            pet_id: Pet ID to delete
            
        Returns:
            True if deleted, False if not found
        """
        pet = db.query(Pet).filter(Pet.id == pet_id).first()
        
        if not pet:
            return False
        
        db.delete(pet)
        db.commit()
        
        return True