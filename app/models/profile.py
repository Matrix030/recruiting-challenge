"""Database models for face profiles.

This module defines the SQLModel-based models for storing face profiles
and their associated embeddings.
"""

from datetime import datetime
import json
from typing import Optional, List

from sqlmodel import Field, SQLModel, Column, JSON


class ProfileBase(SQLModel):
    """Base model for face profiles with common attributes."""
    
    description: str = Field(
        description="Human-readable description of facial features"
    )
    embedding: List[float] = Field(
        description="512-dimensional face embedding vector",
        sa_column=Column(JSON)  # Store as JSON in database
    )


class Profile(ProfileBase, table=True):
    """Database model for storing face profiles."""
    
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ProfileCreate(ProfileBase):
    """Schema for creating new profiles."""
    pass


class ProfileRead(ProfileBase):
    """Schema for reading profile data."""
    
    id: int
    created_at: datetime


class VerificationResult(SQLModel):
    """Schema for face verification results."""
    
    is_match: bool = Field(description="Whether the faces match")
    score: float = Field(description="Similarity score (1.0 = perfect match)") 