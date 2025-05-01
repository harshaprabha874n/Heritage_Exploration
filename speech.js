// Function for Text-to-Speech
function convertTextToSpeech() {
    let text = document.getElementById("textToSpeech").value;
    let language = document.getElementById("language").value;
    let speech = new SpeechSynthesisUtterance();
    speech.text = text;
    speech.lang = language;
    window.speechSynthesis.speak(speech);
}

// Function for Speech-to-Text
function startSpeechRecognition() {
    let recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = "en-US"; // Change this for multilingual support
    recognition.start();

    recognition.onresult = function(event) {
        let transcript = event.results[0][0].transcript;
        document.getElementById("speechToTextResult").innerText = transcript;
    };

    recognition.onerror = function(event) {
        console.log("Error occurred in recognition: " + event.error);
    };
}
