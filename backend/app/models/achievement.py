"""Achievement model - tracks unlocked achievements/badges"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class AchievementDefinition(Base):
    """Achievement template/definition"""
    
    __tablename__ = "achievement_definitions"
    
    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(100), unique=True, nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    icon = Column(String(255), nullable=True)
    
    def __repr__(self):
        return f"<AchievementDefinition(id={self.id}, slug='{self.slug}', name='{self.name}')>"


class Achievement(Base):
    """Unlocked achievements for a pet"""
    
    __tablename__ = "achievements"
    
    id = Column(Integer, primary_key=True, index=True)
    pet_id = Column(Integer, ForeignKey("pets.id", ondelete="CASCADE"), nullable=False, index=True)
    achievement_def_id = Column(Integer, ForeignKey("achievement_definitions.id"), nullable=False)
    
    unlocked_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    pet = relationship("Pet", backref="unlocked_achievements")
    definition = relationship("AchievementDefinition", backref="unlocked_by")
    
    def __repr__(self):
        return f"<Achievement(pet_id={self.pet_id}, achievement_id={self.achievement_def_id}, unlocked_at={self.unlocked_at})>"