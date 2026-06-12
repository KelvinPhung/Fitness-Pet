"""Friendship model - tracks relationships between pets"""
from sqlalchemy import Column, Integer, DateTime, ForeignKey, String, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.database import Base


class FriendshipStatus(str, enum.Enum):
    """Friendship request status"""
    PENDING = "pending"
    ACCEPTED = "accepted"
    BLOCKED = "blocked"


class Friendship(Base):
    """Friendship between two users' pets"""
    
    __tablename__ = "friendships"
    
    id = Column(Integer, primary_key=True, index=True)
    requester_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    receiver_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    status = Column(String(50), default=FriendshipStatus.PENDING, nullable=False)
    
    requested_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    responded_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    requester = relationship(
        "User",
        foreign_keys=[requester_id],
        backref="friend_requests_sent"
    )
    receiver = relationship(
        "User",
        foreign_keys=[receiver_id],
        backref="friend_requests_received"
    )
    
    def __repr__(self):
        return f"<Friendship(id={self.id}, requester_id={self.requester_id}, receiver_id={self.receiver_id}, status='{self.status}')>"