"""Face analysis service using InsightFace.

This module provides face detection, feature extraction and comparison
functionality using the InsightFace library.
"""

from pathlib import Path
from typing import List, Optional, Tuple

import cv2
import insightface
import numpy as np
from PIL import Image

from app.core.config import CONTEXT_ID, DETECTION_SIZE, FACE_MODEL_NAME
from app.models.profile import VerificationResult


class FaceAnalyzer:
    """Service for face detection and analysis using InsightFace."""

    def __init__(self) -> None:
        """Initialize the face analysis model."""
        self.face_app = insightface.app.FaceAnalysis(name=FACE_MODEL_NAME)
        self.face_app.prepare(ctx_id=CONTEXT_ID, det_size=DETECTION_SIZE)

    def get_face_embedding(self, image: Image.Image) -> Optional[np.ndarray]:
        """Extract face embedding vector from an image.
        
        Args:
            image: PIL Image containing a face
            
        Returns:
            512-dimensional embedding vector if face found, None otherwise
        """
        # Convert PIL to OpenCV format
        img_array = np.array(image)
        img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        
        faces = self.face_app.get(img_bgr)
        if not faces:
            return None
            
        return faces[0].embedding

    def analyze_face(self, image: Image.Image) -> Tuple[str, Optional[List[float]]]:
        """Analyze facial features and generate description.
        
        Args:
            image: PIL Image containing a face
            
        Returns:
            Tuple of (description string, embedding vector if face found)
        """
        # Convert PIL to OpenCV format
        img_array = np.array(image)
        img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        
        faces = self.face_app.get(img_bgr)
        
        if not faces:
            return "No face detected in the image.", None
        
        face = faces[0]
        
        # Extract facial measurements
        bbox = face.bbox
        landmarks = face.kps
        embedding = face.embedding.tolist()
        
        # Calculate metrics
        face_width = bbox[2] - bbox[0]
        face_height = bbox[3] - bbox[1]
        face_ratio = face_height / face_width
        
        # Eye measurements
        left_eye = landmarks[0]
        right_eye = landmarks[1]
        eye_distance = np.linalg.norm(right_eye - left_eye)
        eye_face_ratio = eye_distance / face_width
        
        # Nose position
        nose = landmarks[2]
        nose_y_pos = (nose[1] - bbox[1]) / face_height
        
        # Mouth measurements
        left_mouth = landmarks[3]
        right_mouth = landmarks[4]
        mouth_width = np.linalg.norm(right_mouth - left_mouth)
        mouth_face_ratio = mouth_width / face_width
        
        # Generate description
        description = (
            f"Face dimensions: {face_ratio:.2f} height/width ratio. "
            f"Eye spacing: {eye_face_ratio:.3f} relative to face width. "
            f"Nose positioned at {nose_y_pos:.3f} vertical face ratio. "
            f"Mouth width: {mouth_face_ratio:.3f} relative to face width. "
            f"Landmark confidence: {len(faces)} face(s) detected."
        )
        
        return description, embedding

    def verify_faces(
        self, probe_embedding: List[float], ref_embedding: List[float]
    ) -> VerificationResult:
        """Compare two face embeddings and determine if they match.
        
        Args:
            probe_embedding: Embedding vector of probe image
            ref_embedding: Embedding vector of reference image
            
        Returns:
            VerificationResult with match status and similarity score
        """
        # Convert to numpy arrays
        probe = np.array(probe_embedding)
        ref = np.array(ref_embedding)
        
        # Compute cosine similarity
        similarity = np.dot(probe, ref) / (np.linalg.norm(probe) * np.linalg.norm(ref))
        score = float(similarity)  # Convert to native Python float
        
        # Compare against threshold from config
        from app.core.config import SIMILARITY_THRESHOLD
        is_match = score >= SIMILARITY_THRESHOLD
        
        return VerificationResult(is_match=is_match, score=score) 