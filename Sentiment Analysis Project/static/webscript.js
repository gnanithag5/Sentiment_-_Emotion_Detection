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
                document.getElementById("system_response").innerHTML = 
                    `The given text has been identified as <b>${response.sentiment.label.toUpperCase()}</b> with a score of <b>${response.sentiment.score.toFixed(5)}</b>.`;
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

    xhttp.open("GET", "sentimentAnalyzer?textToAnalyze=" + encodeURIComponent(textToAnalyze), true);
    xhttp.send();
};
