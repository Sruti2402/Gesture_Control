import cv2
import mediapipe as mp
import numpy as np
import screen_brightness_control as sbc
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

prev_y = None
tip_ids = [4, 8, 12, 16, 20]
sensitivity = 0.4

def count_fingers(hand_landmarks):
    fingers = []
    for i in range(1, 3):
        if hand_landmarks.landmark[tip_ids[i]].y < hand_landmarks.landmark[tip_ids[i]-2].y:
            fingers.append(1)
        else:
            fingers.append(0)
    return sum(fingers)

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            fingers_up = count_fingers(hand_landmarks)

            index_finger_y = hand_landmarks.landmark[8].y * h

            if prev_y is not None and fingers_up in [1, 2]:
                dy = prev_y - index_finger_y
                if abs(dy) > 3:
                    if fingers_up == 1:
                        current = sbc.get_brightness(display=0)[0]
                        change = int(dy * sensitivity)
                        sbc.set_brightness(max(0, min(100, current + change)))
                    elif fingers_up == 2:
                        current_vol = volume.GetMasterVolumeLevelScalar()
                        change = dy * sensitivity / 100
                        volume.SetMasterVolumeLevelScalar(
                            max(0.0, min(1.0, current_vol + change)), None
                        )

            prev_y = index_finger_y

    cv2.imshow("Finger Control", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
