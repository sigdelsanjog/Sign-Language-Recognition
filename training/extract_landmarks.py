import os
import cv2
import pandas as pd
import time
import concurrent.futures
import mediapipe as mp
import warnings
import utils.free_resources as free_resources  # Import the new module
import utils.log_progress as log_progress  # Import the log progress module

# Suppress warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore")  # Suppress all warnings, including TensorFlow

# Mediapipe initialization
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1)

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

# Function to process a single image
def process_image(letter, image_file):
    image_path = os.path.join(data_dir, letter, image_file)
    landmarks = extract_hand_landmarks(image_path)
    return landmarks, letter

# Directory paths
data_dir = "dataset_1G/"  # Ensure this path is correct
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

# Excel file for logging progress
progress_excel = 'landmark_extraction_timesheet.xlsx'
tab_name = "22GB"  # Change this value as needed

# Create a ThreadPoolExecutor for parallel processing
max_workers = 7  # Adjust based on your system's capabilities
with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
    futures = []
    for letter in letters:
        letter_dir = os.path.join(data_dir, letter)
        if not os.path.exists(letter_dir):
            print(f"Warning: Directory {letter_dir} does not exist. Skipping.")
            continue
        for image_file in os.listdir(letter_dir):
            futures.append(executor.submit(process_image, letter, image_file))

    # Collect results as they complete
    for future in concurrent.futures.as_completed(futures):
        processed_images += 1
        landmarks, letter = future.result()
        if landmarks:
            landmark_data.append(landmarks)
            labels.append(letter)

        # Log progress every 1000 images
        if processed_images % 1000 == 0:
            current_elapsed_time = time.time() - start_time
            print(f"Processed {processed_images}/{total_images} images. Elapsed time: {current_elapsed_time:.2f} seconds.")

            # Call the logging function
            log_progress.calc_landmark_extraction_time(processed_images, current_elapsed_time, tab_name, progress_excel)

# Convert the data to a DataFrame and save it
if landmark_data:
    df = pd.DataFrame(landmark_data)
    df['label'] = labels
    output_csv = 'Llandmarks.csv'
    df.to_csv(output_csv, index=False)
    print(f"Landmark extraction completed. Data saved to {output_csv}.")
else:
    print("No landmarks were extracted. Please check your dataset and Mediapipe setup.")

# End timing
end_time = time.time()
total_time = end_time - start_time
print(f"Total time taken for landmark extraction: {total_time:.2f} seconds ({total_time/60:.2f} minutes).")

hands.close()

# Free resources after program ends
free_resources.clear_memory_caches()
free_resources.clear_tensorflow_session()
free_resources.kill_python_processes()
