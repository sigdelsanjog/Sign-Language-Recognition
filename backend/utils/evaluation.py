import os
import numpy as np
import cv2
import pandas as pd
from tensorflow.keras.models import load_model
from backend.mediapipe_utils import detect_hand_landmarks  # Ensure this function is in utils

# Load the trained model
model_path = '../training/models/sign_language_model.h5'  # Update if needed
model = load_model(model_path)

# Correct the path to the test images directory (since evaluation.py and test_images are in utils/)
test_images_path = os.path.join(os.path.dirname(__file__), 'test_images')

test_labels = []  # Correct labels for test images
images = []
filenames = []

# Load test images and labels
for filename in os.listdir(test_images_path):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        image_path = os.path.join(test_images_path, filename)
        image = cv2.imread(image_path)

        if image is None:  # Check if image loading was successful
            print(f"Error loading image: {filename}")
            continue

        # Detect hand landmarks
        hand_landmarks = detect_hand_landmarks(image)
        
        if hand_landmarks is not None and hand_landmarks.any():
            hand_landmarks = np.array(hand_landmarks).reshape(1, -1)  # Reshape to (1, 63)
            images.append(hand_landmarks)
            filenames.append(filename)
            
            # Assuming label is in the format 'N_test.jpg', 'X_test.jpg', etc.
            label = filename.split('_')[0].upper()
            if label == "NOTHING":
                label = 26  # Assuming "Nothing" gesture is represented by label 26
            else:
                label = ord(label) - 65  # Convert A-Z to 0-25
            
            test_labels.append(label)

# Convert to numpy arrays
if len(images) > 0:
    images = np.vstack(images)
    test_labels = np.array(test_labels)

    # Run predictions
    predictions = model.predict(images)
    predicted_classes = np.argmax(predictions, axis=1)

    # Calculate accuracy
    correct_predictions = np.sum(predicted_classes == test_labels)
    accuracy = correct_predictions / len(test_labels) * 100

    # Create a tabular format using pandas DataFrame
    data = {
        "Filename": filenames,
        "True Label": [chr(label + 65) if label != 26 else "Nothing" for label in test_labels],
        "Predicted Label": [chr(predicted + 65) if predicted != 26 else "Nothing" for predicted in predicted_classes]
    }
    df = pd.DataFrame(data)

    # Print the DataFrame and accuracy
    print(df.to_string(index=False))  # Print DataFrame without the index
    print(f"\nModel accuracy on test set: {accuracy:.2f}%")
else:
    print("No valid hand landmarks detected in test images.")
