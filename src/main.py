from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from io import BytesIO
from PIL import Image
import numpy as np
import cv2
import insightface

app = FastAPI()

# Initialize face analysis model
face_app = insightface.app.FaceAnalysis(name='buffalo_l')
face_app.prepare(ctx_id=0, det_size=(640, 640))  # ctx_id=0 uses GPU

class Profile(BaseModel):
    description: str

@app.post("/create-profile", response_model=Profile)
async def create_profile(file: UploadFile = File(...)):
    img = Image.open(BytesIO(await file.read()))
    profile_description = analyze_face(img)
    return {"description": profile_description}

def analyze_face(image):
    # Convert PIL to OpenCV format
    img_array = np.array(image)
    img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    
    # Detect faces and extract features
    faces = face_app.get(img_bgr)
    
    if not faces:
        return "No face detected in the image."
    
    face = faces[0]  # Use first detected face
    
    # Extract facial measurements and features
    bbox = face.bbox
    landmarks = face.kps
    
    # Calculate facial metrics
    face_width = bbox[2] - bbox[0]
    face_height = bbox[3] - bbox[1]
    face_ratio = face_height / face_width
    
    # Eye distance and position
    left_eye = landmarks[0]
    right_eye = landmarks[1]
    eye_distance = np.linalg.norm(right_eye - left_eye)
    eye_face_ratio = eye_distance / face_width
    
    # Nose position
    nose = landmarks[2]
    nose_y_pos = (nose[1] - bbox[1]) / face_height
    
    # Mouth position  
    left_mouth = landmarks[3]
    right_mouth = landmarks[4]
    mouth_width = np.linalg.norm(right_mouth - left_mouth)
    mouth_face_ratio = mouth_width / face_width
    
    # Generate profile description
    profile = f"Face dimensions: {face_ratio:.2f} height/width ratio. "
    profile += f"Eye spacing: {eye_face_ratio:.3f} relative to face width. "
    profile += f"Nose positioned at {nose_y_pos:.3f} vertical face ratio. "
    profile += f"Mouth width: {mouth_face_ratio:.3f} relative to face width. "
    profile += f"Landmark confidence: {len(faces)} face(s) detected."
    
    return profile