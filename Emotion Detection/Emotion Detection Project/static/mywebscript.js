let RunSentimentAnalysis = () => {
    let textToAnalyze = document.getElementById("textToAnalyze").value.trim();

    // Check if the input is empty or just spaces
    if (textToAnalyze.length === 0) {
        alert("Please enter some text for analysis.");
        return;
    }

    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4) {
            if (this.status == 200) {
                let response = JSON.parse(xhttp.responseText);
                document.getElementById("system_response").innerHTML = `
                    <p>The given text has been identified as <b>${response.emotions.dominant_emotion.toUpperCase()}</b>.</p>
                    <p><b>Emotion Scores:</b></p>
                    <ul>
                        <li><b>Anger:</b> ${response.emotions.anger}</li>
                        <li><b>Disgust:</b> ${response.emotions.disgust}</li>
                        <li><b>Fear:</b> ${response.emotions.fear}</li>
                        <li><b>Joy:</b> ${response.emotions.joy}</li>
                        <li><b>Sadness:</b> ${response.emotions.sadness}</li>
                    </ul>
                `;
            } else if (this.status == 422 || this.status == 400) {
                let response = JSON.parse(xhttp.responseText);
                document.getElementById("system_response").innerHTML = 
                    `<span style="color: red;">Error: ${response.error}</span>`;
            } else {
                document.getElementById("system_response").innerHTML = 
                    `<span style="color: red;">An unexpected error occurred. Please try again.</span>`;
            }
        }
    };

    xhttp.open("GET", "emotionAnalyzer?textToAnalyze=" + encodeURIComponent(textToAnalyze), true);
    xhttp.send();
};
