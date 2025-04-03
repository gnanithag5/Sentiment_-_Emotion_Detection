from flask import Flask, render_template, request, jsonify
from EmotionDetection.emotion_detection import emotion_analyzer  # Importing the correct function

# Initialize the Flask application
app = Flask(__name__)

# Route for rendering the HTML template
@app.route("/")
def render_index_page():
    return render_template('index2.html')

# Route for handling emotion analysis
@app.route("/emotionAnalyzer")
def emotion_analyzer_route():
    # Retrieve the text to analyze from the request arguments (sent from JS)
    text_to_analyze = request.args.get('textToAnalyze')

    # Debugging: print the received text
    print(f"Received text to analyze: '{text_to_analyze}'")

    # Check if the text is not empty or just spaces
    if not text_to_analyze or text_to_analyze.strip() == '':
        return jsonify({"error": "Text is empty, please provide some text for emotion analysis."}), 400
    
    # Call the emotion analyzer function and get the response
    try:
        response = emotion_analyzer(text_to_analyze)
        print(f"Response from emotion analyzer: {response}")  # Debugging output

        # If the response contains an error, return it with status 422
        if 'error' in response:
            return jsonify(response), 422
        
        # Format the result as JSON
        result = {
            'emotions': {
                'anger': response['anger'],
                'disgust': response['disgust'],
                'fear': response['fear'],
                'joy': response['joy'],
                'sadness': response['sadness'],
                'dominant_emotion': response['dominant_emotion']
            }
        }
        
        return jsonify(result), 200

    except Exception as e:
        print(f"Error during emotion analysis: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

# Run the application on localhost:5000
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
