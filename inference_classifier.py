import os
import tensorflow as tf
import pickle
import cv2
import mediapipe as mp
import numpy as np
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# Load the model
with open("C:/Users/ANANDHU/flutter project/X/VAHI/updated code/model.p", 'rb') as file:
    model_dict = pickle.load(file)
model = model_dict['model']

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

# Define labels dictionary
labels_dict = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J', 10: 'K', 11: 'L', 12: 'M', 13: 'N', 14: 'O', 15: 'P', 16: 'Q', 17: 'R', 18: 'S', 19: 'T', 20: 'U', 21: 'V', 22: 'W', 23: 'X', 24: 'Y', 25: 'Z'}

# Try different camera indices and API preferences
camera_indices = [0, 1, 2]
api_preferences = [cv2.CAP_AVFOUNDATION, cv2.CAP_DSHOW, cv2.CAP_MSMF, cv2.CAP_V4L2]

for index in camera_indices:
    for api in api_preferences:
        cap = cv2.VideoCapture(index, api)
        if cap.isOpened():
            print(f"Successfully opened camera with index {index} and API {api}")
            break
    if cap.isOpened():
        break

if not cap.isOpened():
    print("Error: Could not open video source.")
    exit()

while True:
    data_aux = []
    x_ = []
    y_ = []

    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture frame.")
        break

    H, W, _ = frame.shape

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(frame_rgb)
    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame,  # image to draw
                hand_landmarks,  # model output
                mp_hands.HAND_CONNECTIONS,  # hand connections
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style()
            )

            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y

                x_.append(x)
                y_.append(y)

            x_min, x_max = min(x_), max(x_)
            y_min, y_max = min(y_), max(y_)

            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                data_aux.append(x - x_min)
                data_aux.append(y - y_min)

            # Ensure data_aux has exactly 42 features
            if len(data_aux) == 42:
                prediction = model.predict([np.asarray(data_aux)])
                predicted_character = labels_dict[int(prediction[0])]

                x1 = int(x_min * W) - 10
                y1 = int(y_min * H) - 10
                x2 = int(x_max * W) + 10
                y2 = int(y_max * H) + 10

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
                cv2.putText(frame, predicted_character, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3, cv2.LINE_AA)
            else:
                print(f"Warning: data_aux has {len(data_aux)} features, expected 42.")
    cv2.putText(frame, 'Exit? Press "Q" ! :)', (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
