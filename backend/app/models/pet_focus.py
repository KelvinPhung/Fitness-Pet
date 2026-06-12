"""Pet Focus model - tracks which stats the user prioritizes"""
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class PetFocus(Base):
    """
    Focus distribution for pet specialization
    Determines how XP is split between different stat types
    Example: Strength 50%, Endurance 30%, Speed 20%
    """
    
    __tablename__ = "pet_focus"
    
    id = Column(Integer, primary_key=True, index=True)
    pet_id = Column(Integer, ForeignKey("pets.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    
    strength_focus = Column(Integer, default=50, nullable=False)
    endurance_focus = Column(Integer, default=30, nullable=False)
    speed_focus = Column(Integer, default=20, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    pet = relationship("Pet", backref="focus_distribution")
    
    def validate_focus(self) -> bool:
        total = self.strength_focus + self.endurance_focus + self.speed_focus
        return total == 100
    
    def __repr__(self):
        return f"<PetFocus(pet_id={self.pet_id}, strength={self.strength_focus}%, endurance={self.endurance_focus}%, speed={self.speed_focus}%)>"