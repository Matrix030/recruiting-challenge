# Validia Face Recognition API

A FastAPI-based face recognition service that provides face analysis, embedding extraction, and verification capabilities using InsightFace.

## Features

- Face detection and feature analysis
- 512-dimensional face embedding extraction
- Face verification against stored profiles
- RESTful API with OpenAPI documentation
- SQLite persistence with SQLModel
- Modern React frontend with TypeScript
- Docker support
- Pytest-based testing

## Requirements

- Python 3.8+
- Node.js 16+
- InsightFace with buffalo_l model
- CUDA-capable GPU (optional, falls back to CPU)
- Docker (optional)

## Installation

### Backend

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

### Frontend

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

## Usage

### Running the API Server

1. Start the server:
```bash
uvicorn app.main:app --reload
```

2. Access the API documentation at http://localhost:8000/docs

### Running the Frontend

1. Start the development server:
```bash
cd frontend
npm start
```

2. Access the application at http://localhost:3000

### Using Docker

1. Build the images:
```bash
docker-compose build
```

2. Run the services:
```bash
docker-compose up
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

## Frontend Features

The React frontend provides an intuitive interface for:

1. **Profile Creation**
   - Drag-and-drop image upload
   - Real-time face analysis
   - Visual feedback on profile creation

2. **Face Verification**
   - Easy profile selection
   - Visual similarity score
   - Clear match/no-match indication

3. **Profile Management**
   - Grid view of all profiles
   - Pagination support
   - Profile details display

## Testing

Run the backend test suite:
```bash
pytest
```

Run the frontend tests:
```bash
cd frontend
npm test
```

## Ethical Considerations

This face recognition system should be used responsibly:

1. **Consent**: Always obtain explicit consent before collecting and processing facial data.
2. **Privacy**: Store face data securely and only as long as necessary.
3. **Bias**: Be aware that face recognition systems may exhibit demographic biases.
4. **Transparency**: Clearly communicate how face data is used and stored.

## License

MIT License - see LICENSE file for details.

