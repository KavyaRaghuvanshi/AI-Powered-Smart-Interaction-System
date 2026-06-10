from flask import Flask, render_template, Response
import os
import gesture as g
import database as db
import voice as va

va.speak("Welcome to the AI-Powered Smart Interaction System ") 
va.speak("Open the website to start the AI experience")

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/start_ai')
def start_ai():

    va.speak("AI System Activated")

    return "AI System Activated ✅"

@app.route('/analytics')
def analytics_dashboard():
    va.speak("Opening Analytics Dashboard")
    data = db.get_all_interactions()

    return render_template(
        'analytics.html',
        data=data
    )

@app.route('/notepad')
def notepad():

    va.speak("Opening Notepad")

    os.system("notepad")

    return "Notepad Opened Successfully 🚀"

@app.route('/chrome')
def chrome():

    va.speak("Opening Chrome")

    os.startfile(
        "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    )

    return "Chrome Opened Successfully 🚀"

@app.route('/video')
def video():

    return Response(
        g.generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

@app.route('/enable_automation')
def enable_automation():
    va.speak("Gesture automation activated")
    g.automation_enabled = True

    return "Gesture Automation Enabled ✅"


@app.route('/disable_automation')
def disable_automation():
    va.speak("Gesture automation disabled")
    g.automation_enabled = False


    return "Gesture Automation Disabled ❌"

@app.route('/gesture')
def gesture():
    return g.gesture_text

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)