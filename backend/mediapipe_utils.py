import mediapipe as mp
import cv2
import numpy as np

mp_hands = mp.solutions.hands

def detect_hand_landmarks(image):
    hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    result = hands.process(image_rgb)
    hands.close()

    if result.multi_hand_landmarks:
        landmarks = result.multi_hand_landmarks[0].landmark
        return np.array([[lm.x, lm.y, lm.z] for lm in landmarks]).flatten()
    return None
