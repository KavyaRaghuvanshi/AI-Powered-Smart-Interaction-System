import pyttsx3

def speak(text):
    
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 160)
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    
    except Exception as e:
        print(e)