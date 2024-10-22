import pandas as pd
import time
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import precision_score, recall_score, f1_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical
import tensorflow as tf
import numpy as np
import os

# Load the dataset
df = pd.read_csv('landmarks_chunk_5G.csv')

# Separate features and labels
X = df.drop('label', axis=1)
y = df['label']

# Encode labels as integers (A=0, B=1, ..., Z=25)
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# One-hot encode the labels for neural network training
y_categorical = to_categorical(y_encoded, num_classes=29)

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y_categorical, test_size=0.2, random_state=42)

# Create a MirroredStrategy for data parallelism
strategy = tf.distribute.MirroredStrategy()

# Function to log training time, accuracy, precision, recall, F1 score, and time difference to an Excel file
def log_training_progress(epoch, times, accuracies, precisions, recalls, f1_scores, sheet_name="Train_5G"):
    progress_excel = 'training_timesheet.xlsx'
    
    # Create a DataFrame for the current progress
    progress_data = pd.DataFrame({
        'Epoch': [epoch],
        'Elapsed Time (seconds)': [times[-1]],  # Time for the latest epoch
        'Time Difference (seconds)': [times[-1] - times[-2] if len(times) > 1 else None],  # Time difference from the previous epoch
        'Accuracy': [accuracies[-1]],
        'Precision': [precisions[-1]],
        'Recall': [recalls[-1]],
        'F1 Score': [f1_scores[-1]]
    })

    # Debug: print the progress_data being written
    print(f"Logging data to {sheet_name}:")
    print(progress_data)

    # Check if the Excel file exists
    if os.path.exists(progress_excel):
        # Load the existing Excel file
        with pd.ExcelWriter(progress_excel, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
            # Check if the sheet already exists
            if sheet_name in writer.sheets:
                # Get the last row of the existing sheet
                startrow = writer.sheets[sheet_name].max_row
                progress_data.to_excel(writer, sheet_name=sheet_name, index=False, header=False, startrow=startrow)
            else:
                # Create the sheet with headers
                progress_data.to_excel(writer, sheet_name=sheet_name, index=False)
    else:
        # Create a new Excel file and write the data with headers
        with pd.ExcelWriter(progress_excel, engine='openpyxl', mode='w') as writer:
            progress_data.to_excel(writer, sheet_name=sheet_name, index=False)

# Build the neural network model inside the strategy scope
with strategy.scope():
    model = Sequential()
    model.add(Dense(128, input_shape=(X_train.shape[1],), activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(29, activation='softmax'))  # 26 output units for A-Z

    # Compile the model
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Specify number of epochs
num_epochs = 20

# Initialize tracking for timing, accuracy, precision, recall, F1 score
epoch_times = []
epoch_accuracies = []
epoch_precisions = []
epoch_recalls = []
epoch_f1_scores = []

start_time = time.time()

print("Training started...")

# Train the model while tracking time, accuracy, precision, recall, and F1 score for each epoch
for epoch in range(num_epochs):
    epoch_start_time = time.time()
    
    # Train for one epoch
    history = model.fit(X_train, y_train, epochs=1, batch_size=32, validation_data=(X_test, y_test), verbose=1)
    
    # Calculate elapsed time for this epoch
    epoch_end_time = time.time()
    elapsed_time = epoch_end_time - start_time
    epoch_times.append(elapsed_time)

    # Get predictions for validation data
    y_pred = model.predict(X_test)
    y_pred_classes = np.argmax(y_pred, axis=1)
    y_true_classes = np.argmax(y_test, axis=1)
    
    # Calculate precision, recall, and F1 score
    precision = precision_score(y_true_classes, y_pred_classes, average='macro', zero_division=1)
    recall = recall_score(y_true_classes, y_pred_classes, average='macro')
    f1 = f1_score(y_true_classes, y_pred_classes, average='macro')
    
    # Get validation accuracy from the history object
    epoch_accuracy = history.history['val_accuracy'][0]
    epoch_accuracies.append(epoch_accuracy)
    epoch_precisions.append(precision)
    epoch_recalls.append(recall)
    epoch_f1_scores.append(f1)

    print(f"Epoch {epoch + 1}/{num_epochs} completed. Time: {elapsed_time:.2f}s. Accuracy: {epoch_accuracy:.4f}. Precision: {precision:.4f}. Recall: {recall:.4f}. F1 Score: {f1:.4f}")

    # Log the progress immediately after each epoch
    sheet_name = "TrainingRun2"  # Change this name for each training session
    log_training_progress(epoch + 1, epoch_times, epoch_accuracies, epoch_precisions, epoch_recalls, epoch_f1_scores, sheet_name)

# End timing the entire training process
end_time = time.time()
total_time = end_time - start_time

# Print total time taken for training
print(f"Training completed in {total_time:.2f} seconds ({total_time/60:.2f} minutes).")

# Evaluate the model on the test set
test_loss, test_accuracy = model.evaluate(X_test, y_test)
print(f"Test accuracy: {test_accuracy}")

# Save the trained model
model.save('models/sign_language_model_5GB.h5')
model.save('models/sign_language_model_5GB.keras')
print("Model saved as 'models/sign_language_model_5GB.h5'.")
