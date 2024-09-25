import pandas as pd
import time  # Import the time module
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical

# Load the dataset
df = pd.read_csv('sign_language_landmarks.csv')

# Separate features and labels
X = df.drop('label', axis=1)
y = df['label']

# Encode labels as integers (A=0, B=1, ..., Z=25)
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# One-hot encode the labels for neural network training
y_categorical = to_categorical(y_encoded, num_classes=26)

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y_categorical, test_size=0.2, random_state=42)

# Build the neural network model
model = Sequential()
model.add(Dense(128, input_shape=(X_train.shape[1],), activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(26, activation='softmax'))  # 26 output units for A-Z

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Start timing the training process
start_time = time.time()
print("Training started...")

# Train the model, and track the time and progress
history = model.fit(X_train, y_train, epochs=20, batch_size=32, validation_data=(X_test, y_test))

# End timing the training process
end_time = time.time()
total_time = end_time - start_time

# Print total time taken for training
print(f"Training completed in {total_time:.2f} seconds ({total_time/60:.2f} minutes).")

# Evaluate the model on the test set
test_loss, test_accuracy = model.evaluate(X_test, y_test)
print(f"Test accuracy: {test_accuracy}")

# Save the trained model
model.save('models/sign_language_model.h5')
print("Model saved as 'models/sign_language_model.h5'.")
