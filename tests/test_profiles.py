"""Tests for face profile management endpoints."""

import io
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from PIL import Image
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.core.database import get_session
from app.main import app

# Test database
SQLITE_URL = "sqlite://"  # In-memory database

@pytest.fixture
def session():
    """Create a fresh database session for each test."""
    engine = create_engine(
        SQLITE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture
def client(session):
    """Create a test client with a fresh database session."""
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

def get_test_image_path(filename: str) -> Path:
    """Get path to a test image file."""
    return Path(__file__).parent / "data" / filename

def test_create_profile(client):
    """Test creating a face profile from an image."""
    # Create a small test image with a face
    image = Image.new('RGB', (100, 100), color='white')
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    
    response = client.post(
        "/api/v1/profiles",
        files={"file": ("test.png", img_byte_arr, "image/png")}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "description" in data
    assert "embedding" in data
    assert len(data["embedding"]) == 512  # InsightFace embedding size

def test_get_profile(client):
    """Test retrieving a face profile."""
    # First create a profile
    image = Image.new('RGB', (100, 100), color='white')
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    
    create_response = client.post(
        "/api/v1/profiles",
        files={"file": ("test.png", img_byte_arr, "image/png")}
    )
    profile_id = create_response.json()["id"]
    
    # Then retrieve it
    response = client.get(f"/api/v1/profiles/{profile_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == profile_id

def test_verify_face(client):
    """Test face verification against a stored profile."""
    # Create reference profile
    image = Image.new('RGB', (100, 100), color='white')
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    
    create_response = client.post(
        "/api/v1/profiles",
        files={"file": ("ref.png", img_byte_arr, "image/png")}
    )
    profile_id = create_response.json()["id"]
    
    # Verify same image
    img_byte_arr.seek(0)
    verify_response = client.post(
        f"/api/v1/profiles/verify/{profile_id}",
        files={"file": ("probe.png", img_byte_arr, "image/png")}
    )
    
    assert verify_response.status_code == 200
    result = verify_response.json()
    assert "is_match" in result
    assert "score" in result
    assert isinstance(result["score"], float)
    assert 0 <= result["score"] <= 1 