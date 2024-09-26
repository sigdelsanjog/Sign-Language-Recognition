# Hand Gesture Recognition Project

This project is aimed at creating a robust **Hand Gesture Recognition System** using **Mediapipe** and **TensorFlow**. The system can be utilized for real-time gesture recognition in applications such as sign language translation, touchless control, and human-computer interaction.

The project is divided into three major components: **Frontend**, **Backend**, and **Model Training**. Each part plays a crucial role in ensuring the smooth running of the system, from data acquisition and processing to the final gesture prediction.

## Table of Contents
- [Frontend](#frontend)
- [Backend](#backend)
- [Model Training](#model-training)
- [Technologies Used](#technologies-used)

---

## Frontend

The frontend is designed to provide a user-friendly interface for the hand gesture recognition system. It allows users to interact with the system seamlessly while visualizing their gestures.

### Features
- **Webcam Integration**: Real-time video feed captures hand movements.
- **Gesture Visualization**: Displays the recognized gestures in real time.
- **User Interaction**: Allows users to see the output of gesture recognition with a simple and intuitive interface.

### Technologies Used
- **React.js**: A JavaScript library for building user interfaces, providing the core functionality for handling the UI and user interactions.
- **HTML/CSS**: Basic web technologies for structuring and styling the user interface.
- **MediaStream API**: Used for capturing real-time video from the webcam.

### Frontend Workflow
1. **Webcam Input**: The frontend captures the user's hand gestures via a webcam.
2. **Gesture Prediction Display**: Based on the model's predictions, the frontend displays the identified gesture in real-time.
3. **Data Communication**: Sends captured data to the backend for processing.

---

## Backend

The backend handles the core logic for image processing, hand landmark extraction, and gesture classification. It interacts with the trained machine learning model to provide gesture predictions.

### Features
- **Image Processing**: Extracts hand landmarks from images using Mediapipe.
- **Parallel Processing**: Handles large datasets efficiently using concurrent processing.
- **Data Logging**: Logs the time taken for each batch of image processing into an Excel file for performance tracking.
- **Error Handling**: Skips corrupt or missing images during processing.

### Technologies Used
- **Python**: Core programming language used to implement the backend.
- **Mediapipe**: A framework by Google for extracting hand landmarks.
- **OpenCV**: A library for real-time computer vision, used for image processing.
- **Concurrent Futures**: Used to implement multi-threaded processing for handling large datasets efficiently.
- **Pandas**: For data manipulation and logging the processing times in Excel.
- **TensorFlow**: Used for gesture prediction and integration with the trained model.

### Backend Workflow
1. **Hand Landmark Extraction**: Mediapipe extracts hand landmarks from the provided image dataset.
2. **Concurrent Processing**: Processes large datasets in parallel to reduce execution time.
3. **Logging and Reporting**: Logs the time taken for each batch of images and stores the data in an Excel file.

---

## Model Training

The core of the hand gesture recognition system is built around a machine learning model that is trained on a large dataset of hand gestures.

### Features
- **Data Preprocessing**: Cleans and prepares the dataset for training, including normalizing hand landmark data.
- **Model Architecture**: Uses a deep learning model built with TensorFlow/Keras.
- **Training Pipeline**: Efficiently trains the model on the processed hand landmark data.
- **Model Evaluation**: Evaluates the model using various metrics such as accuracy, precision, recall, and confusion matrix.

### Technologies Used
- **TensorFlow/Keras**: The core library used for building, training, and deploying the deep learning model.
- **Mediapipe**: Used to extract landmarks from the gesture dataset.
- **OpenCV**: Helps in image manipulation before feeding it to the model.
- **Numpy**: Provides numerical operations required during data preprocessing.
- **Pandas**: For handling data operations during preprocessing and logging.

### Model Training Workflow
1. **Dataset Preparation**: Prepares the dataset by extracting landmarks and labeling them appropriately.
2. **Model Building**: Builds the deep learning model using TensorFlow/Keras.
3. **Training**: Trains the model on the prepared dataset and evaluates performance metrics.
4. **Model Saving**: Saves the trained model for use in the backend for real-time gesture recognition.

---

## Technologies Used

### Frontend
- **React.js**: Used for building the user interface and managing real-time interactions.
- **HTML5/CSS3**: For structuring and designing the frontend.
- **JavaScript**: For dynamic content updates and integration with MediaStream API.

### Backend
- **Python**: Core programming language for backend development.
- **Mediapipe**: Extracts hand landmarks for gesture recognition.
- **OpenCV**: Provides image processing functionalities.
- **Concurrent Futures**: Manages parallel processing for efficient image handling.
- **Pandas**: Data manipulation and time logging in CSV and Excel formats.
- **TensorFlow**: Powers the machine learning model for gesture recognition.

### Model Training
- **TensorFlow/Keras**: For building, training, and evaluating the gesture recognition model.
- **Mediapipe**: Used for extracting hand landmarks for the training dataset.
- **Numpy**: For efficient numerical operations on landmark data.
- **Pandas**: Handles dataset operations during the training process.

---

### How to Run the Project

1. **Clone the Repository**: `git clone <repo-url>`
2. **Frontend Setup**:
   - Navigate to the frontend folder: `cd frontend`
   - Install dependencies: `npm install`
   - Start the development server: `npm start`
3. **Backend Setup**:
   - Navigate to the backend folder: `cd backend`
   - Create and activate a Python virtual environment.
   - Install the dependencies: `pip install -r requirements.txt`
   - Run the backend: `python backend.py`
4. **Model Training**:
   - Navigate to the training folder: `cd training`
   - Run the training script: `python train_model.py`

---

### Future Work

- **Extended Gesture Set**: Add support for more gestures, including custom ones.
- **Optimized Real-time Prediction**: Improve the latency of real-time gesture recognition.
- **Cross-Platform Deployment**: Deploy the system on mobile and desktop platforms.



# TO DO
- Enable Parallelism for Training Model
- Store data for each threads in CSV similar to extract_landmarks
- Check if extracting landmarks in image processing is a compulsary approach or even if it is widely adapted

Phase II
- Breakdown the image dataset into 1GB 2GB 3GB 4GB 5GB or 78000/1 /2 /3 /4 /5
