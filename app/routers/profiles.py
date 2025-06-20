"""API routes for face profile management.

This module implements the REST API endpoints for creating, retrieving,
and verifying face profiles.
"""

from io import BytesIO
from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from PIL import Image
from sqlmodel import Session, select

from app.core.database import get_session
from app.core.face_analyzer import FaceAnalyzer
from app.models.profile import Profile, ProfileCreate, ProfileRead, VerificationResult

router = APIRouter()
face_analyzer = FaceAnalyzer()

@router.post("/profiles", response_model=ProfileRead, summary="Create a face profile")
async def create_profile(
    file: UploadFile = File(...),
    session: Session = Depends(get_session)
) -> Profile:
    """Create a new face profile from an uploaded image.
    
    Args:
        file: Image file containing a face
        session: Database session
        
    Returns:
        Created profile with ID and metadata
        
    Raises:
        HTTPException: If no face is detected in the image
    """
    try:
        image = Image.open(BytesIO(await file.read()))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image file: {str(e)}")
        
    description, embedding = face_analyzer.analyze_face(image)
    
    if embedding is None:
        raise HTTPException(status_code=400, detail="No face detected in image")
        
    profile = Profile(description=description, embedding=embedding)
    session.add(profile)
    session.commit()
    session.refresh(profile)
    
    return profile

@router.get("/profiles/{profile_id}", response_model=ProfileRead)
def get_profile(
    profile_id: int,
    session: Session = Depends(get_session)
) -> Profile:
    """Retrieve a face profile by ID.
    
    Args:
        profile_id: ID of profile to retrieve
        session: Database session
        
    Returns:
        Face profile data
        
    Raises:
        HTTPException: If profile not found
    """
    profile = session.get(Profile, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.get("/profiles", response_model=List[ProfileRead])
def list_profiles(
    session: Session = Depends(get_session),
    skip: int = 0,
    limit: int = 100
) -> List[Profile]:
    """List all face profiles with pagination.
    
    Args:
        session: Database session
        skip: Number of profiles to skip
        limit: Maximum number of profiles to return
        
    Returns:
        List of face profiles
    """
    profiles = session.exec(
        select(Profile).offset(skip).limit(limit)
    ).all()
    return profiles

@router.post("/verify/{profile_id}", response_model=VerificationResult)
async def verify_face(
    profile_id: int,
    file: UploadFile = File(...),
    session: Session = Depends(get_session)
) -> VerificationResult:
    """Compare an uploaded face image against a stored profile.
    
    Args:
        profile_id: ID of profile to compare against
        file: Image file containing face to verify
        session: Database session
        
    Returns:
        Verification result with match status and similarity score
        
    Raises:
        HTTPException: If profile not found or no face detected
    """
    # Get stored profile
    profile = session.get(Profile, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
        
    # Process uploaded image
    try:
        image = Image.open(BytesIO(await file.read()))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image file: {str(e)}")
        
    probe_embedding = face_analyzer.get_face_embedding(image)
    if probe_embedding is None:
        raise HTTPException(status_code=400, detail="No face detected in image")
        
    # Compare embeddings
    return face_analyzer.verify_faces(
        probe_embedding=probe_embedding.tolist(),
        ref_embedding=profile.embedding
    ) 