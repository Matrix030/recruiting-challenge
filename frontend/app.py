"""Streamlit frontend for the Validia Face Recognition API.

This module provides a user-friendly interface for interacting with the
face recognition API endpoints.
"""

import io
from typing import Optional, Tuple

import requests
import streamlit as st
from PIL import Image

# API Configuration
API_BASE_URL = "http://localhost:8000/api/v1"

def upload_and_display_image() -> Tuple[Optional[Image.Image], Optional[bytes]]:
    """Handle image upload and display.
    
    Returns:
        Tuple of (PIL Image if successful, bytes of image)
    """
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image_bytes = uploaded_file.read()
        image = Image.open(io.BytesIO(image_bytes))
        st.image(image, caption="Uploaded Image", use_column_width=True)
        return image, image_bytes
    return None, None

def create_profile(image_bytes: bytes) -> dict:
    """Create a new face profile.
    
    Args:
        image_bytes: Raw image data
        
    Returns:
        Profile data from API
    """
    files = {"file": ("image.jpg", image_bytes, "image/jpeg")}
    response = requests.post(f"{API_BASE_URL}/profiles", files=files)
    response.raise_for_status()
    return response.json()

def get_profiles() -> list:
    """Get list of all profiles.
    
    Returns:
        List of profile data
    """
    response = requests.get(f"{API_BASE_URL}/profiles")
    response.raise_for_status()
    return response.json()

def verify_face(profile_id: int, image_bytes: bytes) -> dict:
    """Verify a face against a stored profile.
    
    Args:
        profile_id: ID of profile to compare against
        image_bytes: Raw image data to verify
        
    Returns:
        Verification result from API
    """
    files = {"file": ("image.jpg", image_bytes, "image/jpeg")}
    response = requests.post(
        f"{API_BASE_URL}/profiles/verify/{profile_id}",
        files=files
    )
    response.raise_for_status()
    return response.json()

# Streamlit UI
st.title("👤 Validia Face Recognition Demo")

# Sidebar navigation
page = st.sidebar.selectbox(
    "Choose a function",
    ["Create Profile", "View Profiles", "Verify Face"]
)

try:
    if page == "Create Profile":
        st.header("Create New Face Profile")
        st.write("""
        Upload a face image to create a new profile. The system will:
        1. Detect the face in the image
        2. Extract facial features and measurements
        3. Generate a 512-dimensional face embedding
        4. Store the profile for later verification
        """)
        
        image, image_bytes = upload_and_display_image()
        
        if image is not None and st.button("Create Profile"):
            with st.spinner("Creating profile..."):
                profile = create_profile(image_bytes)
                st.success("Profile created successfully!")
                st.json(profile)

    elif page == "View Profiles":
        st.header("View Stored Profiles")
        st.write("List of all face profiles in the database:")
        
        if st.button("Refresh Profiles"):
            with st.spinner("Loading profiles..."):
                profiles = get_profiles()
                for profile in profiles:
                    with st.expander(f"Profile {profile['id']}"):
                        st.write("Description:", profile["description"])
                        st.write("Created:", profile["created_at"])

    else:  # Verify Face
        st.header("Verify Face")
        st.write("""
        Compare a new face image against a stored profile to check if they match.
        The system will:
        1. Extract face embedding from the new image
        2. Compare it with the stored profile's embedding
        3. Calculate a similarity score
        """)
        
        # Get list of profiles for selection
        profiles = get_profiles()
        profile_ids = [p["id"] for p in profiles]
        
        if not profile_ids:
            st.warning("No profiles found. Please create a profile first.")
        else:
            selected_id = st.selectbox(
                "Select profile to compare against:",
                profile_ids
            )
            
            image, image_bytes = upload_and_display_image()
            
            if image is not None and st.button("Verify Face"):
                with st.spinner("Verifying..."):
                    result = verify_face(selected_id, image_bytes)
                    
                    if result["is_match"]:
                        st.success(f"✅ Match found! Similarity score: {result['score']:.3f}")
                    else:
                        st.error(f"❌ No match. Similarity score: {result['score']:.3f}")

except requests.exceptions.ConnectionError:
    st.error("""
    ⚠️ Could not connect to the API server!
    
    Please make sure the API server is running:
    ```bash
    uvicorn app.main:app --reload
    ```
    """)
except Exception as e:
    st.error(f"An error occurred: {str(e)}")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("""
### About
This demo showcases the Validia Face Recognition API capabilities:
- Face detection & analysis
- Feature extraction
- Face verification
""") 