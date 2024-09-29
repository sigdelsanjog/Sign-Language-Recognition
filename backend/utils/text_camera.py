import cv2

cap = cv2.VideoCapture('/dev/video0')  # or /dev/video1
if not cap.isOpened():
    print(f"Error: Camera at /dev/video0 could not be opened.")
else:
    print("Camera opened successfully!")
    cap.release()
