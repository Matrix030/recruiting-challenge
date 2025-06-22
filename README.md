# Validia Face Recognition API

A robust face recognition system that creates unique facial profiles and provides verification capabilities. Built with FastAPI and InsightFace, this system offers high-accuracy face detection, feature extraction, and similarity matching.

## Key Features

- **Face Detection & Analysis**: Extracts 512-dimensional face embeddings using InsightFace
- **Profile Creation**: Generates detailed facial feature descriptions and stores embeddings
- **Face Verification**: Compares faces using cosine similarity with configurable thresholds
- **Interactive Demo**: Streamlit-based UI for easy testing and visualization
- **GPU Acceleration**: CUDA support for faster processing (with CPU fallback)

## Architecture

### Backend (FastAPI)
- **Core Components**:
  - Face Analyzer: InsightFace integration for face processing
  - Database: SQLite with SQLModel for profile storage
  - Configuration: Environment-based settings

- **API Endpoints**:
  ```
  POST /api/v1/profiles           # Create face profile
  GET  /api/v1/profiles          # List all profiles
  GET  /api/v1/profiles/{id}     # Get specific profile
  POST /api/v1/profiles/verify/{id} # Verify face against profile
  ```

### Frontend (Streamlit)
- Profile creation interface
- Profile browsing and management
- Face verification with visual feedback
- Real-time similarity scoring

## Getting Started

###Prerequisites
- Python 3.8+
- CUDA-capable GPU (optional)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Matrix030/recruiting-challenge.git
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate    # Windows
```

3. Install dependencies (use uv for faster installation):
```bash
pip install -r requirements.txt
```

### Running the Application

1. Start the API server:
```bash
uvicorn app.main:app --reload
```

2. Launch the frontend (in a new terminal):
```bash
streamlit run frontend/app.py
```

3. Access:
- API Documentation: http://localhost:8000/docs
- Frontend Interface: http://localhost:8501

## Implementation Details

### Face Analysis Pipeline

1. **Face Detection**
   - Uses InsightFace's SCRFD detector
   - Handles multiple face scenarios (selects primary face)
   - Provides confidence scores

2. **Feature Extraction**
   - 512-dimensional embedding vector
   - Facial landmarks (eyes, nose, mouth)
   - Geometric measurements:
     - Face ratio (height/width)
     - Eye spacing
     - Nose position
     - Mouth width

3. **Verification Process**
   - Cosine similarity between embeddings
   - Configurable threshold (default: 0.6)
   - Returns match status and similarity score

### Data Storage

- **Profile Schema**:
  ```python
  class Profile:
      id: int
      description: str
      embedding: List[float]  # 512-D vector
      created_at: datetime
  ```

- **Storage Method**: SQLite with JSON serialization for embeddings
- **Performance**: Optimized for quick similarity comparisons

## 🔧 Configuration

Key settings in `app/core/config.py`:
```python
FACE_MODEL_NAME: str = "buffalo_l"
DETECTION_SIZE: tuple[int, int] = (640, 640)
SIMILARITY_THRESHOLD: float = 0.6
```

Environment variables:
- `USE_GPU`: Enable/disable GPU acceleration (default: true)
- `SQLITE_URL`: Database connection string
- `SIMILARITY_THRESHOLD`: Custom matching threshold


### Data Privacy
- No raw images are stored
- Only feature vectors and metadata retained
- Local database by default

### Create Profile
```http
POST /api/v1/profiles
Content-Type: multipart/form-data

file: <image_file>
```

### Verify Face
```http
POST /api/v1/profiles/verify/{profile_id}
Content-Type: multipart/form-data

file: <image_file>
```

Response:
```json
{
    "is_match": true,
    "score": 0.95
}
```

## Future Improvements

1. **Scalability**
   - Redis caching for frequent verifications
   - Distributed processing support

2. **Features**
   - Batch processing API
   - Age and gender estimation
   - Expression analysis
   - Multiple face handling
   - Multimodel scanning to aggregate outputs of multiple models running in parallel 
   - If all four modules—Biometrics, Deepfake Detection, and Liveness Checks—are successfully passed, we save the embedding from that session, as there is a chance that the biometric score was just above the threshold. Storing such embeddings helps enrich the user’s profile, leading to more accurate biometric verification in future sessions. 

3. **Security**
   - Rate limiting
   - API key authentication
   - Audit logging

## Reference:
https://medium.com/@appanamukesh77/comprehensive-insights-onfacial-analysis-with-insightface-library-796d80464f45
https://insightface.ai/