from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import cv2
from utils.mediapipe_utils import detect_hand_landmarks
from tensorflow.keras.models import load_model
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
    
    # Debugging: Print the image shape to verify proper image loading
    if image is not None:
        print(f"Image shape: {image.shape}")
    else:
        return {"error": "Failed to decode image"}

    # Check for valid image shape
    if image is None or image.shape[0] == 0 or image.shape[1] == 0:
        return {"error": "Invalid image data"}

    # Detect hand landmarks using Mediapipe utils
    hand_landmarks = detect_hand_landmarks(image)

    # Debugging: Print the status of hand landmarks detection
    if hand_landmarks is not None and len(hand_landmarks) > 0:
        print(f"Hand landmarks detected: {hand_landmarks}")

        # Reshape the hand landmarks for model input
        hand_landmarks = np.array(hand_landmarks).reshape(1, -1)  # Reshape to (1, 63)
        print(f"Reshaped landmarks: {hand_landmarks.shape}")

        # Predict the sign language alphabet based on landmarks
        prediction = model.predict(hand_landmarks)
        predicted_class = np.argmax(prediction, axis=1)[0]
        return {"sign": chr(65 + predicted_class)}  # A-Z corresponds to 0-25
    else:
        print("No hand detected")
    
    return {"error": "No hand detected"}

