function startAI() {

    fetch('/start_ai')
    .then(response => response.text())
    .then(data => {

    document.getElementById("status").innerHTML = data;
    document.getElementById("video-feed").src = "/video";

    });

}

function openChrome() {

    fetch('/chrome')
    .then(response => response.text())
    .then(data => {

        document.getElementById("status").innerHTML = data;

    });

}

function openNotepad() {

    fetch('/notepad')
    .then(response => response.text())
    .then(data => {

        document.getElementById("status").innerHTML = data;

    });

}

function enableAutomation() {

    fetch('/enable_automation')
    .then(response => response.text())
    .then(data => {

        document.getElementById("status").innerHTML = data;

    });

}

function disableAutomation() {

    fetch('/disable_automation')
    .then(response => response.text())
    .then(data => {

        document.getElementById("status").innerHTML = data;

    });

}

function openAnalytics() {

    window.location.href = "/analytics";

}

setInterval(() => {

    fetch('/gesture')
    .then(response => response.text())
    .then(data => {

        document.getElementById("gestureText").innerHTML =
            "Detected Gesture: " + data;

    });

}, 500);