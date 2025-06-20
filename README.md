# Validia Face Recognition API

A FastAPI-based face recognition service that provides face analysis, embedding extraction, and verification capabilities using InsightFace.

## Features

- Face detection and feature analysis
- 512-dimensional face embedding extraction
- Face verification against stored profiles
- RESTful API with OpenAPI documentation
- SQLite persistence with SQLModel
- Docker support
- Pytest-based testing
- Streamlit frontend demo

## Requirements

- Python 3.8+
- InsightFace with buffalo_l model
- CUDA-capable GPU (optional, falls back to CPU)
- Docker (optional)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/validia-face-recognition.git
cd validia-face-recognition
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the API Server

1. Start the server:
```bash
uvicorn app.main:app --reload
```

2. Access the API documentation at http://localhost:8000/docs

### Running the Frontend Demo

1. Make sure the API server is running (see above)

2. In a new terminal, start the Streamlit frontend:
```bash
streamlit run frontend/app.py
```

3. Open your browser to http://localhost:8501

The frontend demo provides an intuitive interface for:
- Creating face profiles from images
- Viewing stored profiles
- Verifying faces against stored profiles

### Using Docker

1. Build the image:
```bash
docker build -t validia-face-api .
```

2. Run the container:
```bash
docker run -p 8000:8000 validia-face-api
```

## API Endpoints

### POST /api/v1/profiles
Create a new face profile from an uploaded image.

**Request:**
- Multipart form with 'file' field containing the image

**Response:**
```json
{
    "id": 1,
    "description": "Face analysis description...",
    "embedding": [...],
    "created_at": "2024-03-21T12:00:00"
}
```

### POST /api/v1/verify/{profile_id}
Verify a face against a stored profile.

**Request:**
- URL parameter: profile_id
- Multipart form with 'file' field containing the probe image

**Response:**
```json
{
    "is_match": true,
    "score": 0.95
}
```

### GET /api/v1/profiles/{profile_id}
Retrieve a stored face profile.

### GET /api/v1/profiles
List all stored profiles with pagination.

## Face Verification Thresholds

The system uses cosine similarity between face embeddings to determine matches:

- Score > 0.6: Considered a match
- Score < 0.6: Not a match

This threshold was chosen based on InsightFace's recommendations and empirical testing. It provides a good balance between:
- False accept rate (FAR)
- False reject rate (FRR)

## Testing

Run the test suite:
```bash
pytest
```

For verbose output:
```bash
pytest -v
```

## Ethical Considerations

This face recognition system should be used responsibly:

1. **Consent**: Always obtain explicit consent before collecting and processing facial data.
2. **Privacy**: Store face data securely and only as long as necessary.
3. **Bias**: Be aware that face recognition systems may exhibit demographic biases.
4. **Transparency**: Clearly communicate how face data is used and stored.

## License

MIT License - see LICENSE file for details.

