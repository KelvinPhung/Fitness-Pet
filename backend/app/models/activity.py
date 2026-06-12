"""Activity model - logs user's fitness activities"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.database import Base


class ActivityType(str, enum.Enum):
    """Supported activity types"""
    RUNNING = "running"
    WALKING = "walking"
    CYCLING = "cycling"
    SWIMMING = "swimming"
    STRENGTH_TRAINING = "strength_training"
    YOGA = "yoga"
    SPORTS = "sports"
    HIIT = "hiit"
    CARDIO = "cardio"
    OTHER = "other"


class Activity(Base):
    """Activity model for fitness tracking"""
    
    __tablename__ = "activities"
    
    id = Column(Integer, primary_key=True, index=True)
    pet_id = Column(Integer, ForeignKey("pets.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    activity_type = Column(String(50), nullable=False)
    distance = Column(Float, default=0, nullable=False)
    duration = Column(Integer, nullable=False)
    intensity = Column(String(50), default="moderate", nullable=False)
    
    strength_xp = Column(Integer, default=0, nullable=False)
    endurance_xp = Column(Integer, default=0, nullable=False)
    speed_xp = Column(Integer, default=0, nullable=False)
    total_xp = Column(Integer, default=0, nullable=False)
    
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    pet = relationship("Pet", backref="activity_log")
    user = relationship("User", backref="activities")
    
    def __repr__(self):
        return f"<Activity(id={self.id}, type='{self.activity_type}', distance={self.distance}km, duration={self.duration}min, total_xp={self.total_xp})>"