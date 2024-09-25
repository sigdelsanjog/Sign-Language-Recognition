import os
import mediapipe as mp
import cv2
import numpy as np
import pandas as pd

# Mediapipe initialization
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1)
mp_drawing = mp.solutions.drawing_utils

# Function to extract hand landmarks
def extract_hand_landmarks(image_path):
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    result = hands.process(image_rgb)
    
    if result.multi_hand_landmarks:
        hand_landmarks = result.multi_hand_landmarks[0]
        landmarks = []
        for lm in hand_landmarks.landmark:
            landmarks.extend([lm.x, lm.y, lm.z])
        return landmarks
    return None

# Directory paths
data_dir = "dataset/"
letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

# Initialize list to store the data
landmark_data = []
labels = []

# Loop over each folder (each letter)
for letter in letters:
    letter_dir = os.path.join(data_dir, letter)
    for image_file in os.listdir(letter_dir):
        image_path = os.path.join(letter_dir, image_file)
        landmarks = extract_hand_landmarks(image_path)
        if landmarks:
            landmark_data.append(landmarks)
            labels.append(letter)

# Convert the data to a DataFrame and save it
df = pd.DataFrame(landmark_data)
df['label'] = labels
df.to_csv('sign_language_landmarks.csv', index=False)

hands.close()
