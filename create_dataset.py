import os
import pickle

import mediapipe as mp
import cv2
import matplotlib.pyplot as plt


mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

DATA_DIR = "data"

data = []
labels = []
for dir_ in os.listdir(DATA_DIR):
    if dir_ == '.DS_Store':
        continue  # Skip .DS_Store file

    dir_path = os.path.join(DATA_DIR, dir_)
    print(f"Processing directory: {dir_path}")

    for img_path in os.listdir(dir_path):
        full_path = os.path.join(dir_path, img_path)
        print(f"Processing image: {full_path}")
        
        data_aux = []
        x_ = []
        y_ = []

        img = cv2.imread(full_path)
        if img is None:
            print(f"Error: Could not read image {full_path}")
            continue
            
        try:
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = hands.process(img_rgb)
            
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    for i in range(len(hand_landmarks.landmark)):
                        x = hand_landmarks.landmark[i].x
                        y = hand_landmarks.landmark[i].y
                        x_.append(x)
                        y_.append(y)

                    for i in range(len(hand_landmarks.landmark)):
                        x = hand_landmarks.landmark[i].x
                        y = hand_landmarks.landmark[i].y
                        data_aux.append(x - min(x_))
                        data_aux.append(y - min(y_))

                data.append(data_aux)
                labels.append(dir_)
                print(f"Successfully processed {img_path}")
        except Exception as e:
            print(f"Error processing {img_path}: {str(e)}")
            continue

# Save data with error handling
try:
    with open('data.pickle', 'wb') as f:
        pickle.dump({'data': data, 'labels': labels}, f)
    print(f"Successfully saved {len(data)} samples")
except Exception as e:
    print(f"Error saving data: {str(e)}")
