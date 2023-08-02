from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import mediapipe as mp
import cv2
import numpy as np
import time
import requests
import json

# Path to the Brave browser executable
brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"

# Set up Chrome options to use Brave browser
option = webdriver.ChromeOptions()
option.binary_location = brave_path

# Set up Chrome service using the ChromeDriverManager
s = Service(ChromeDriverManager().install())

# Define the joint points and initial angle for each finger for two hands
fingers = {1: {"Index": {"joint_points": [7, 6, 5], "angle": 0},
               "Middle": {"joint_points": [11, 10, 9], "angle": 0},
               "Ring": {"joint_points": [15, 14, 13], "angle": 0},
               "Pinky": {"joint_points": [19, 18, 17], "angle": 0},
               "Thumb": {"joint_points": [3, 2, 1], "angle": 0}},
           2: {"Index": {"joint_points": [7, 6, 5], "angle": 0},
               "Middle": {"joint_points": [11, 10, 9], "angle": 0},
               "Ring": {"joint_points": [15, 14, 13], "angle": 0},
               "Pinky": {"joint_points": [19, 18, 17], "angle": 0},
               "Thumb": {"joint_points": [3, 2, 1], "angle": 0}}}

# Define the gesture per second variables
frame_no = 0
mf = {"var": 0, "frames": [], "detected": False}
mfx2 = {"var": 0, "frames": [], "detected": False}
idf = {"var": 0, "frames": [], "detected": False}
pf = {"var": 0, "frames": [], "detected": False}
yof = {"var": 0, "frames": [], "detected": False}
number_of_hands = {"now": 0, "prev": 0}
X = 15
m = 12


# Function to get the label of the hand (left or right)
def get_label(index, hand, results):
    output = None
    for idx, classification in enumerate(results.multi_handedness):
        if classification.classification[0].index == index:
            label = classification.classification[0].label
            score = classification.classification[0].score
            text = '{} {}'.format(label, round(score, 2))

            coords = tuple(np.multiply(
                np.array((hand.landmark[mp_hands.HandLandmark.WRIST].x,
                          hand.landmark[mp_hands.HandLandmark.WRIST].y)),
                [640, 480]).astype(int))

            output = text, coords

    return output


# Function to draw the angles of the fingers on the opencv camera feed
def draw_finger_angles(image, results, fingers, number_of_hands):
    number_of_hands["prev"] = number_of_hands["now"]
    number_of_hands["now"] = len(results.multi_hand_landmarks)
    if len(results.multi_hand_landmarks) > 2:
        return image

    if number_of_hands["prev"] > number_of_hands["now"]:
        fingers[2]["Index"]["angle"] = 0
        fingers[2]["Middle"]["angle"] = 0
        fingers[2]["Ring"]["angle"] = 0
        fingers[2]["Pinky"]["angle"] = 0
        fingers[2]["Thumb"]["angle"] = 0

    for hand_landmark in results.multi_hand_landmarks:
        hand = results.multi_hand_landmarks.index(hand_landmark) + 1

        for finger in fingers[hand]:
            joint = fingers[hand][finger]["joint_points"]
            a = np.array([hand_landmark.landmark[joint[0]].x, hand_landmark.landmark[joint[0]].y])
            b = np.array([hand_landmark.landmark[joint[1]].x, hand_landmark.landmark[joint[1]].y])
            c = np.array([hand_landmark.landmark[joint[2]].x, hand_landmark.landmark[joint[2]].y])

            radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
            angle = np.abs(radians * 180.0 / np.pi)

            if angle > 180.0:
                angle = 360 - angle

            fingers[hand][finger]["angle"] = angle
            # print(f"Angle of {finger} is {fingers[finger]['angle']}.")

            cv2.putText(image, str(round(angle, 2)), tuple(np.multiply(b, [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    determine_gesture_per_second(fingers)
    # print(fingers)
    return image


# Function to determine the gesture in a second
def determine_gesture_per_second(fingers):
    global mf
    global mfx2
    global idf
    global pf
    global yof

    index_1 = fingers[1]["Index"]["angle"]
    middle_1 = fingers[1]["Middle"]["angle"]
    ring_1 = fingers[1]["Ring"]["angle"]
    pinky_1 = fingers[1]["Pinky"]["angle"]
    thumb_1 = fingers[1]["Thumb"]["angle"]
    index_2 = fingers[2]["Index"]["angle"]
    middle_2 = fingers[2]["Middle"]["angle"]
    ring_2 = fingers[2]["Ring"]["angle"]
    pinky_2 = fingers[2]["Pinky"]["angle"]
    thumb_2 = fingers[2]["Thumb"]["angle"]

    # Double Middle Finger detection
    if (index_1 < 120 and middle_1 > 150 and ring_1 < 90 and pinky_1 < 90) and \
            (index_2 < 120 and middle_2 > 150 and ring_2 < 90 and pinky_2 < 90):
        mfx2["detected"] = True
        mfx2["var"] += 1
        if mfx2["var"] <= X:
            mfx2["frames"].append(mfx2["detected"])
        if mfx2["var"] > X:
            if mfx2["frames"].count(True) >= m:
                print(f'DOUBLE MIDDLE FINGER, {mfx2["frames"].count(True)}')
            mfx2["frames"] = []
            mfx2["var"] = 0
    # Middle Finger detection
    elif (index_1 < 120 and middle_1 > 150 and ring_1 < 90 and pinky_1 < 90) or \
            (index_2 < 120 and middle_2 > 150 and ring_2 < 90 and pinky_2 < 90):
        mf["detected"] = True
        mf["var"] += 1
        if mf["var"] <= X:
            mf["frames"].append(mf["detected"])
        if mf["var"] > X:
            if mf["frames"].count(True) >= m:
                print(f'MIDDLE FINGER, {mf["frames"].count(True)}')
                url = 'http://192.168.1.3:5069/jsonex'
                data = {
                    "appliance": "f"
                }
                json_data = json.dumps(data)
                requests.post(url, data=json_data, headers={'Content-Type': 'application/json'})
                # browser = webdriver.Chrome(service=s, options=option)
                # browser.get("http://192.168.1.3:5069")
                # browser.find_element(By.ID, "fan_button").click()
                # browser.quit()
            mf["frames"] = []
            mf["var"] = 0
    else:
        mf["detected"] = False
        if mf["var"] >= 1:
            mf["var"] += 1
            mf["frames"].append(mf["detected"])
        mfx2["detected"] = False
        if mfx2["var"] >= 1:
            mfx2["var"] += 1
            mfx2["frames"].append(mfx2["detected"])

    # Index Finger detection
    if (index_1 > 150 and middle_1 < 90 and ring_1 < 90 and pinky_1 < 90) or \
            (index_2 > 150 and middle_2 < 90 and ring_2 < 90 and pinky_2 < 90):
        idf["detected"] = True
        idf["var"] += 1
        if idf["var"] <= X:
            idf["frames"].append(idf["detected"])
        if idf["var"] > X:
            if idf["frames"].count(True) >= m:
                print(f'INDEX FINGER, {idf["frames"].count(True)}')
                url = 'http://192.168.1.3:5069/jsonex'
                data = {
                    "appliance": "bl"
                }
                json_data = json.dumps(data)
                requests.post(url, data=json_data, headers={'Content-Type': 'application/json'})
                # browser = webdriver.Chrome(service=s, options=option)
                # browser.get("http://192.168.91.53:5069")
                # browser.find_element(By.ID, "back_light_button").click()
                # browser.quit()
            idf["frames"] = []
            idf["var"] = 0
    else:
        idf["detected"] = False
        if idf["var"] >= 1:
            idf["var"] += 1
            idf["frames"].append(idf["detected"])

    # Pinky Finger detection
    if (index_1 < 90 and middle_1 < 90 and ring_1 < 90 and pinky_1 > 150) or \
            (index_2 < 90 and middle_2 < 90 and ring_2 < 90 and pinky_2 > 150):
        pf["detected"] = True
        pf["var"] += 1
        if pf["var"] <= X:
            pf["frames"].append(pf["detected"])
        if pf["var"] > X:
            if pf["frames"].count(True) >= m:
                print(f'PINKY FINGER, {pf["frames"].count(True)}')
                url = 'http://192.168.1.3:5069/jsonex'
                data = {
                    "appliance": "tl"
                }
                json_data = json.dumps(data)
                requests.post(url, data=json_data, headers={'Content-Type': 'application/json'})
                # browser = webdriver.Chrome(service=s, options=option)
                # browser.get("http://192.168.91.53:5069")
                # browser.find_element(By.ID, "top_light_button").click()
                # browser.quit()
            pf["frames"] = []
            pf["var"] = 0
    else:
        pf["detected"] = False
        if pf["var"] >= 1:
            pf["var"] += 1
            pf["frames"].append(pf["detected"])

    # YO gesture detection
    if (index_1 > 150 and middle_1 < 90 and ring_1 < 90 and pinky_1 > 150) or \
            (index_2 > 150 and middle_2 < 90 and ring_2 < 90 and pinky_2 > 150):
        yof["detected"] = True
        yof["var"] += 1
        if yof["var"] <= X:
            yof["frames"].append(yof["detected"])
        if yof["var"] > X:
            if yof["frames"].count(True) >= m:
                print(f'YO, {yof["frames"].count(True)}')
            yof["frames"] = []
            yof["var"] = 0
    else:
        yof["detected"] = False
        if yof["var"] >= 1:
            yof["var"] += 1
            yof["frames"].append(yof["detected"])


time.sleep(2)

# Initialize the drawing and hand modules from MediaPipe
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Start capturing video from the webcam
cap = cv2.VideoCapture(1)

# Start the hand detection
with mp_hands.Hands(min_detection_confidence=0.2, min_tracking_confidence=0.2) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = cv2.flip(image, 1)
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for num, hand in enumerate(results.multi_hand_landmarks):
                mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(0, 0, 255),
                                                                 thickness=2, circle_radius=2),
                                          mp_drawing.DrawingSpec(color=(224, 224, 224),
                                                                 thickness=2, circle_radius=2))

                if get_label(num, hand, results):
                    text, coord = get_label(num, hand, results)
                    cv2.putText(image, text, coord,
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)

            frame_no += 1
            # print(f"FRAME NUMBER {frame_no}")
            draw_finger_angles(image, results, fingers, number_of_hands)

        cv2.imshow('op', image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
