# app/core/profiler.py
from typing import Tuple
import face_recognition
import numpy as np

def create_profile(image) -> Tuple[np.ndarray, str]:
    # 1. Detect first face
    img = np.array(image.convert("RGB"))
    locs   = face_recognition.face_locations(img, model="hog")
    if not locs:
        raise ValueError("No face detected")
    # 2. Encode (128-dim vector)
    encoding = face_recognition.face_encodings(img, known_face_locations=locs)[0]
    # 3. Derive a human description – simple landmark heuristics for now
    landmarks = face_recognition.face_landmarks(img, face_locations=locs)[0]
    cheeks_high = "high" if max(pt[1] for pt in landmarks["chin"]) - min(pt[1] for pt in landmarks["chin"]) < 80 else "medium"
    desc = f"Oval face, {cheeks_high} cheekbones, {len(landmarks['left_eye'])}-point eye contour."
    return encoding, desc
