from fer import FER

# Emotion detector
detector = FER()

emotion_text = "No Emotion"

def detect_emotion(frame):

    global emotion_text

    emotions = detector.detect_emotions(frame)

    for emotion in emotions:

        emotion_data = emotion["emotions"]

        detected_emotion = max(
            emotion_data,
            key=emotion_data.get
        )

        emotion_text = detected_emotion

    return emotion_text