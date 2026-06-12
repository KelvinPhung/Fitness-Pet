"""Pet database model"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.database import Base


class PetSpecies(str, enum.Enum):
    """Available pet species"""
    DOG = "dog"
    CAT = "cat"
    RABBIT = "rabbit"
    BIRD = "bird"
    DRAGON = "dragon"


class Pet(Base):
    """Pet model for user's virtual companion"""
    
    __tablename__ = "pets"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    species = Column(String(50), nullable=False)
    
    level = Column(Integer, default=1, nullable=False)
    experience = Column(Integer, default=0, nullable=False)
    evolution_stage = Column(Integer, default=1, nullable=False)
    
    strength_xp = Column(Integer, default=0, nullable=False)
    endurance_xp = Column(Integer, default=0, nullable=False)
    speed_xp = Column(Integer, default=0, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    user = relationship("User", backref="pets")
    pet_focus = relationship("PetFocus", uselist=False, backref="pet", cascade="all, delete-orphan")
    activities = relationship("Activity", backref="pet", cascade="all, delete-orphan")
    achievements = relationship("Achievement", backref="pet", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Pet(id={self.id}, name='{self.name}', species='{self.species}', level={self.level}, stage={self.evolution_stage})>"