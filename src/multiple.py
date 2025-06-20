# Cell 1: Imports & FastAPI setup
from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from io import BytesIO
from PIL import Image
import numpy as np
import hashlib
import logging
from typing import Dict, List, Optional

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Cell 2: Initialize InsightFace models with error handling
from insightface.app import FaceAnalysis

# Use only models that are actually available in 2025
# curricular_face and magface_r100 are no longer available from InsightFace
PREFERRED_MODELS = ["buffalo_l"]  # Only use buffalo_l which is confirmed working
apps = {}

def initialize_model(name: str, max_retries: int = 2) -> Optional[FaceAnalysis]:
    """Initialize a single model with retry logic and error handling."""
    for attempt in range(max_retries):
        try:
            logger.info(f"Attempting to initialize model: {name} (attempt {attempt + 1})")
            fa = FaceAnalysis(name=name, providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
            fa.prepare(ctx_id=0)  # GPU context
            logger.info(f"Successfully initialized model: {name}")
            return fa
        except Exception as e:
            logger.warning(f"Failed to initialize {name} on attempt {attempt + 1}: {str(e)}")
            if attempt == max_retries - 1:
                logger.error(f"Failed to initialize {name} after {max_retries} attempts")
                return None
    return None

# Initialize models
logger.info("Starting model initialization...")
for name in PREFERRED_MODELS:
    fa = initialize_model(name)
    if fa is not None:
        apps[name] = fa
    else:
        logger.warning(f"Skipping model {name} due to initialization failure")

# Ensure we have at least one working model
if not apps:
    raise RuntimeError("No face analysis models could be initialized")

logger.info(f"Successfully initialized {len(apps)} models: {list(apps.keys())}")

# Cell 3: Helper functions for embeddings, hashing & aggregation
def hash_embedding(emb: np.ndarray) -> str:
    """Create a hash of the embedding for uniqueness checking."""
    b = emb.astype(np.float32).tobytes()
    return hashlib.sha256(b).hexdigest()

def cosine_similarity(u: np.ndarray, v: np.ndarray) -> float:
    """Calculate cosine similarity between two vectors."""
    return float(np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v)))

def get_embeddings(img_np: np.ndarray) -> Dict[str, np.ndarray]:
    """
    Returns a dict { model_name: embedding_array } for the first detected face.
    Only uses successfully initialized models.
    """
    embs = {}
    face_detected = False
    
    for name, fa in apps.items():
        try:
            faces = fa.get(img_np)
            if faces and len(faces) > 0:
                embs[name] = faces[0].embedding
                face_detected = True
                logger.debug(f"Got embedding from {name}: shape {faces[0].embedding.shape}")
            else:
                logger.warning(f"No face detected by {name}")
        except Exception as e:
            logger.error(f"Error getting embedding from {name}: {str(e)}")
    
    if not face_detected:
        raise ValueError("No face detected by any available model")
    
    return embs

def aggregate_embeddings(embs: Dict[str, np.ndarray], weights: Optional[Dict[str, float]] = None) -> np.ndarray:
    """
    Simple weighted average of embeddings.
    If weights not provided, uses equal weighting.
    """
    if not embs:
        raise ValueError("No embeddings to aggregate")
    
    if weights is None:
        weights = {name: 1.0 / len(embs) for name in embs}
    
    # Normalize weights to sum to 1
    total_weight = sum(weights.get(name, 0) for name in embs)
    if total_weight == 0:
        raise ValueError("Total weight cannot be zero")
    
    normalized_weights = {name: weights.get(name, 0) / total_weight for name in embs}
    
    # Calculate weighted average
    agg = sum(normalized_weights[name] * embs[name] for name in embs)
    return agg

# Cell 4: Response models
class Profile(BaseModel):
    embeddings: Dict[str, List[float]]  # per-model embeddings
    aggregated: List[float]  # fused embedding
    hash: str  # hash of aggregated embedding
    landmarks: List[List[float]]  # facial landmarks
    models_used: List[str]  # which models were successfully used
    confidence_scores: Dict[str, float]  # confidence per model (if available)

# Cell 5: Main face analysis function
def analyze_face(pil_img: Image.Image) -> Dict:
    """
    Analyze a face image and return comprehensive profile data.
    """
    try:
        # Convert PIL image to numpy array
        img = np.array(pil_img.convert("RGB"))
        
        # Get embeddings from all available models
        embs = get_embeddings(img)
        
        if not embs:
            raise ValueError("No embeddings could be extracted")
        
        # Aggregate embeddings
        agg = aggregate_embeddings(embs)
        
        # Get landmarks from the first available model
        landmarks = []
        confidence_scores = {}
        
        # Try to get landmarks and confidence from each model
        for name, fa in apps.items():
            try:
                faces = fa.get(img)
                if faces and len(faces) > 0:
                    face = faces[0]
                    if not landmarks and hasattr(face, 'kps'):
                        landmarks = face.kps.tolist()
                    
                    # Some models provide confidence/detection scores
                    if hasattr(face, 'det_score'):
                        confidence_scores[name] = float(face.det_score)
                    else:
                        confidence_scores[name] = 1.0  # Default confidence
            except Exception as e:
                logger.warning(f"Could not get additional data from {name}: {str(e)}")
        
        # Create hash of aggregated embedding
        emb_hash = hash_embedding(agg)
        
        return {
            "embeddings": {name: emb.tolist() for name, emb in embs.items()},
            "aggregated": agg.tolist(),
            "hash": emb_hash,
            "landmarks": landmarks,
            "models_used": list(embs.keys()),
            "confidence_scores": confidence_scores
        }
        
    except Exception as e:
        logger.error(f"Error in analyze_face: {str(e)}")
        raise HTTPException(status_code=422, detail=f"Face analysis failed: {str(e)}")

# Cell 6: FastAPI endpoints
@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "models_available": list(apps.keys()),
        "total_models": len(apps)
    }

@app.get("/models")
async def get_models():
    """Get information about loaded models."""
    return {
        "loaded_models": list(apps.keys()),
        "total_loaded": len(apps),
        "attempted_models": PREFERRED_MODELS
    }

@app.post("/create-profile", response_model=Profile)
async def create_profile(file: UploadFile = File(...)):
    """
    Create a face profile from an uploaded image.
    Returns embeddings, landmarks, and other face data.
    """
    # Validate file type
    if not file.content_type or not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Read and process image
        image_data = await file.read()
        img = Image.open(BytesIO(image_data))
        
        # Analyze the face
        profile_data = analyze_face(img)
        
        return Profile(**profile_data)
        
    except Exception as e:
        logger.error(f"Error processing upload: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

# Cell 7: Additional utility endpoints
@app.post("/compare-faces")
async def compare_faces(file1: UploadFile = File(...), file2: UploadFile = File(...)):
    """
    Compare two face images and return similarity scores.
    """
    try:
        # Process both images
        img1_data = await file1.read()
        img2_data = await file2.read()
        
        img1 = Image.open(BytesIO(img1_data))
        img2 = Image.open(BytesIO(img2_data))
        
        profile1 = analyze_face(img1)
        profile2 = analyze_face(img2)
        
        # Calculate similarities
        similarities = {}
        
        # Compare aggregated embeddings
        agg1 = np.array(profile1["aggregated"])
        agg2 = np.array(profile2["aggregated"])
        similarities["aggregated"] = cosine_similarity(agg1, agg2)
        
        # Compare individual model embeddings
        for model in profile1["embeddings"]:
            if model in profile2["embeddings"]:
                emb1 = np.array(profile1["embeddings"][model])
                emb2 = np.array(profile2["embeddings"][model])
                similarities[f"model_{model}"] = cosine_similarity(emb1, emb2)
        
        return {
            "similarities": similarities,
            "models_compared": list(profile1["models_used"]),
            "same_person_likely": similarities["aggregated"] > 0.6  # Threshold can be adjusted
        }
        
    except Exception as e:
        logger.error(f"Error comparing faces: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Comparison failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)