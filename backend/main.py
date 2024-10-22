from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import numpy as np
import cv2
from mediapipe_utils import detect_hand_landmarks
from tensorflow.keras.models import load_model
from gtts import gTTS
import os

app = FastAPI()

# Allowing CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Construct the relative path to the model
model_path = os.path.join(os.path.dirname(__file__), '../training/models/sign_language_model.h5')

# Load pre-trained sign language model
model = load_model(model_path)

@app.post("/predict")
async def predict_sign(file: UploadFile = File(...)):
    # Read and decode the uploaded image
    image_data = await file.read()
    image_np = np.frombuffer(image_data, np.uint8)
    image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
    
    # Check for valid image shape
    if image is None or image.shape[0] == 0 or image.shape[1] == 0:
        return {"error": "Invalid image data"}

    # Detect hand landmarks using Mediapipe utils
    hand_landmarks = detect_hand_landmarks(image)

    # Debugging: Print the status of hand landmarks detection
    if hand_landmarks is not None and len(hand_landmarks) > 0:
        # Reshape the hand landmarks for model input
        hand_landmarks = np.array(hand_landmarks).reshape(1, -1)  # Reshape to (1, 63)

        # Predict the sign language alphabet based on landmarks
        prediction = model.predict(hand_landmarks)
        predicted_class = np.argmax(prediction, axis=1)[0]
        predicted_sign = chr(65 + predicted_class)
        print(f"Predicted sign: {predicted_sign}")  # Log prediction

        # Generate TTS for the predicted sign
        tts = gTTS(text=predicted_sign, lang='en')
        audio_path = os.path.join(os.path.dirname(__file__), 'output.mp3')
        tts.save(audio_path)

        return {"sign": predicted_sign, "audio_url": "/audio/output.mp3"}  # Include audio URL
    else:
        return {"error": "No hand detected"}

@app.get("/audio/{filename}")
async def get_audio(filename: str):
    file_path = os.path.join(os.path.dirname(__file__), filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="audio/mpeg")
    return {"error": "Audio file not found"}

@app.post("/start_detection")
async def start_detection(background_tasks: BackgroundTasks):
    background_tasks.add_task(start_periodic_prediction)
    return {"status": "Detection started"}

@app.post("/stop_detection")
async def stop_detection():
    # Implement stop logic if necessary
    return {"status": "Detection stopped"}

def start_periodic_prediction():
    # This function is a placeholder as the camera will not be accessed in the backend.
    print("Periodic prediction will be handled by the frontend.")
