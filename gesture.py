import cv2
import mediapipe as mp
import time
import automation as auto
import emotion
import database as db


# MediaPipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

mp_draw = mp.solutions.drawing_utils

# Finger tip IDs
tip_ids = [4, 8, 12, 16, 20]

# Webcam
camera = cv2.VideoCapture(0)

# Global variables
gesture_text = "AI Not Started"
last_gesture = ""
last_action_time = 0
voice_cooldown = 3
cooldown = 8
automation_enabled = False


def generate_frames():

    global gesture_text
    global last_gesture
    global last_action_time

    emotion_counter=0
    detected_emotion = "Unknown"
    
    while True:

        success, frame = camera.read()

        if not success:
            break

        # Flip frame
        frame = cv2.flip(frame, 1)

        # Resize frame
        frame = cv2.resize(frame, (960, 540))

        # Convert BGR → RGB
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        emotion_counter += 1

        if emotion_counter % 15 == 0:
            detected_emotion = emotion.detect_emotion(frame)
        
        # Detect hands
        result = hands.process(rgb)
        
        landmarks = []

        
        cv2.putText(frame,  f'Emotion: {detected_emotion}',(30, 140),cv2.FONT_HERSHEY_SIMPLEX,1,(0, 255, 255),2)

        if result.multi_hand_landmarks:
            
            for hand_landmarks in result.multi_hand_landmarks:

                # Draw hand landmarks
                mp_draw.draw_landmarks(frame,hand_landmarks,mp_hands.HAND_CONNECTIONS)

                # Get coordinates
                for id, lm in enumerate(hand_landmarks.landmark):

                    h, w, c = frame.shape

                    cx = int(lm.x * w)
                    cy = int(lm.y * h)

                    landmarks.append([id, cx, cy])

                    cv2.circle(frame,(cx, cy),5,(255, 0, 0),cv2.FILLED)

        # Finger detection
        if len(landmarks) != 0:
            fingers = []

            # Thumb
            if landmarks[4][1] > landmarks[3][1]:
                fingers.append(1)
            else:
                fingers.append(0)

            # Other fingers
            for tip in range(1, 5):

                if landmarks[tip_ids[tip]][2] < landmarks[tip_ids[tip] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            # Count fingers
            total_fingers = fingers.count(1)

            # Gesture names
            if total_fingers == 1:
                gesture_text = "Calculator"

            elif total_fingers == 2:
                gesture_text = "File Explorer"
            
            elif total_fingers == 3:
                gesture_text = "Calendar"

            elif total_fingers == 4:
                gesture_text = "Terminal"

            elif total_fingers == 5:
                gesture_text = "Settings"

            else:
                gesture_text = "No Gesture"

                
            # Cooldown for actions
            current_time = time.time()

            if automation_enabled and current_time - last_action_time > cooldown:
                if gesture_text != last_gesture:
                    if total_fingers == 1:
                        auto.open_calculator()
                        db.save_interaction(gesture_text,detected_emotion,"Calculator Opened")

                    elif total_fingers == 2:
                        auto.open_file_explorer()
                        db.save_interaction(gesture_text, detected_emotion, "File Explorer Opened")

                    elif total_fingers == 3:
                        auto.open_calendar()
                        db.save_interaction(gesture_text, detected_emotion, "Calendar Opened")

                    elif total_fingers == 4:
                        auto.open_terminal()
                        db.save_interaction(gesture_text, detected_emotion, "Terminal Opened")

                    elif total_fingers == 5:
                        auto.open_settings()
                        db.save_interaction(gesture_text, detected_emotion, "Settings Opened")
                        
                last_gesture = gesture_text
                last_action_time = current_time

            # Fingers
            cv2.putText(frame,f'Fingers: {total_fingers}',(30, 50),cv2.FONT_HERSHEY_SIMPLEX,1,(0, 255, 0),2)

            # Gesture
            cv2.putText(frame,f'Gesture: {gesture_text}',(30, 95),cv2.FONT_HERSHEY_SIMPLEX,1,(255, 255, 255),2)



        # Convert frame
        ret, buffer = cv2.imencode('.jpg', frame)

        frame = buffer.tobytes()

        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' +frame +b'\r\n')
