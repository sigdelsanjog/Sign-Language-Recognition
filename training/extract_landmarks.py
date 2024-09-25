import os
import mediapipe as mp
import cv2
import numpy as np
import pandas as pd
import time  # Import the time module

# Mediapipe initialization
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1)
mp_drawing = mp.solutions.drawing_utils

# Function to extract hand landmarks
def extract_hand_landmarks(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print(f"Warning: Unable to read image at {image_path}. Skipping.")
        return None
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
data_dir = "dataset1G/"  # Ensure this path is correct
letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

# Initialize lists to store the data
landmark_data = []
labels = []

# Start timing
start_time = time.time()
print("Starting landmark extraction...")

# Initialize a counter for progress logging
total_images = 0
processed_images = 0

# First, calculate total number of images for progress estimation
for letter in letters:
    letter_dir = os.path.join(data_dir, letter)
    if not os.path.exists(letter_dir):
        print(f"Error: Directory {letter_dir} does not exist. Please check your dataset path.")
        continue
    image_files = [f for f in os.listdir(letter_dir) if os.path.isfile(os.path.join(letter_dir, f))]
    total_images += len(image_files)

print(f"Total images to process: {total_images}")

# Loop over each folder (each letter)
for letter in letters:
    letter_dir = os.path.join(data_dir, letter)
    if not os.path.exists(letter_dir):
        print(f"Warning: Directory {letter_dir} does not exist. Skipping.")
        continue
    for image_file in os.listdir(letter_dir):
        image_path = os.path.join(letter_dir, image_file)
        landmarks = extract_hand_landmarks(image_path)
        if landmarks:
            landmark_data.append(landmarks)
            labels.append(letter)
        processed_images += 1

        # Log progress every 10,000 images
        if processed_images % 1000 == 0:
            elapsed = time.time() - start_time
            print(f"Processed {processed_images}/{total_images} images. Elapsed time: {elapsed:.2f} seconds.")

# Convert the data to a DataFrame and save it
if landmark_data:
    df = pd.DataFrame(landmark_data)
    df['label'] = labels
    output_csv = 'sign_language_landmarks.csv'
    df.to_csv(output_csv, index=False)
    print(f"Landmark extraction completed. Data saved to {output_csv}.")
else:
    print("No landmarks were extracted. Please check your dataset and Mediapipe setup.")

# End timing
end_time = time.time()
total_time = end_time - start_time
print(f"Total time taken for landmark extraction: {total_time:.2f} seconds ({total_time/60:.2f} minutes).")

hands.close()
