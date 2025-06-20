import streamlit as st
import requests
import numpy as np
import cv2
from PIL import Image
import insightface

# Initialize face analysis model (for frontend visualization)
@st.cache_resource
def load_face_model():
    face_app = insightface.app.FaceAnalysis(name='buffalo_l')
    face_app.prepare(ctx_id=-1, det_size=(640, 640))  # Use CPU for frontend
    return face_app

def analyze_face_local(image):
    """Local face analysis for visualization"""
    face_app = load_face_model()
    img_array = np.array(image)
    img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    faces = face_app.get(img_bgr)
    return faces

def draw_landmarks(image, faces):
    """Draw landmarks on the image"""
    img_with_landmarks = np.array(image.copy())
    
    for face in faces:
        landmarks = face.kps
        bbox = face.bbox
        
        # Draw bounding box
        cv2.rectangle(img_with_landmarks, 
                     (int(bbox[0]), int(bbox[1])), 
                     (int(bbox[2]), int(bbox[3])), 
                     (0, 255, 0), 2)
        
        # Draw landmarks
        for point in landmarks:
            cv2.circle(img_with_landmarks, 
                      (int(point[0]), int(point[1])), 
                      3, (255, 0, 0), -1)
    
    return Image.fromarray(img_with_landmarks)

# Streamlit App
st.set_page_config(
    page_title="Validia Face Profile Creator",
    page_icon="👤",
    layout="wide"
)

st.title("👤 Validia Face Profile Creator")
st.markdown("Upload an image to create a detailed facial profile for authenticity verification")

# Sidebar
st.sidebar.header("Settings")
api_url = st.sidebar.text_input("API URL", value="http://127.0.0.1:8000")
show_landmarks = st.sidebar.checkbox("Show Facial Landmarks", value=True)

# Main interface
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📤 Upload Image")
    uploaded_file = st.file_uploader(
        "Choose an image file",
        type=['png', 'jpg', 'jpeg'],
        help="Upload a clear photo with a visible face"
    )
    
    if uploaded_file is not None:
        # Display original image
        image = Image.open(uploaded_file)
        st.image(image, caption="Original Image", use_column_width=True)
        
        # Show image info
        st.info(f"**Image Size:** {image.size[0]} x {image.size[1]} pixels")

with col2:
    st.header("🔍 Analysis Results")
    
    if uploaded_file is not None:
        try:
            # Call the FastAPI endpoint
            files = {"file": uploaded_file.getvalue()}
            with st.spinner("Analyzing facial features..."):
                response = requests.post(f"{api_url}/create-profile", files=files)
            
            if response.status_code == 200:
                result = response.json()
                profile_description = result["description"]
                
                # Display profile in a nice format
                st.success("✅ Face Profile Created Successfully!")
                st.text_area("Facial Profile", value=profile_description, height=150)
                
                # Show landmarks if enabled
                if show_landmarks:
                    with st.spinner("Detecting facial landmarks..."):
                        faces = analyze_face_local(image)
                        if faces:
                            img_with_landmarks = draw_landmarks(image, faces)
                            st.image(img_with_landmarks, 
                                   caption="Image with Facial Landmarks", 
                                   use_column_width=True)
                            
                            # Show detection stats
                            st.metric("Faces Detected", len(faces))
                        else:
                            st.warning("No faces detected for landmark visualization")
                
                # Parse and display metrics
                if "Face dimensions:" in profile_description:
                    lines = profile_description.split(". ")
                    metrics = {}
                    
                    for line in lines:
                        if "height/width ratio" in line:
                            ratio = float(line.split(":")[1].split()[0])
                            metrics["Face Ratio"] = f"{ratio:.2f}"
                        elif "Eye spacing:" in line:
                            eye_ratio = float(line.split(":")[1].split()[0])
                            metrics["Eye Spacing"] = f"{eye_ratio:.3f}"
                        elif "Nose positioned at" in line:
                            nose_pos = float(line.split("at")[1].split()[0])
                            metrics["Nose Position"] = f"{nose_pos:.3f}"
                        elif "Mouth width:" in line:
                            mouth_ratio = float(line.split(":")[1].split()[0])
                            metrics["Mouth Width"] = f"{mouth_ratio:.3f}"
                    
                    # Display metrics in columns
                    if metrics:
                        st.subheader("📊 Key Measurements")
                        metric_cols = st.columns(len(metrics))
                        for i, (key, value) in enumerate(metrics.items()):
                            metric_cols[i].metric(key, value)
                
            else:
                st.error(f"❌ API Error: {response.status_code}")
                st.text(response.text)
                
        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot connect to API. Make sure the FastAPI server is running.")
            st.code("uvicorn main:app --reload")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# Footer
st.markdown("---")
st.markdown("### 🚀 How to Use")
st.markdown("""
1. **Start the API**: Run `uvicorn main:app --reload` in your terminal
2. **Upload Image**: Choose a clear photo with a visible face
3. **View Profile**: Get detailed facial measurements and landmarks
4. **Use Profile**: The generated profile can be used to verify authenticity of other images
""")

st.markdown("### 🛠️ API Status")
if st.button("Test API Connection"):
    try:
        response = requests.get(f"{api_url}/docs")
        if response.status_code == 200:
            st.success("✅ API is running successfully!")
        else:
            st.error("❌ API returned unexpected status")
    except:
        st.error("❌ Cannot reach API server")