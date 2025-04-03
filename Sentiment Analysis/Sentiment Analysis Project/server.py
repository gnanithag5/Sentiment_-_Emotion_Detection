from flask import Flask, render_template, request, jsonify
from SentimentAnalysis.sentiment_analysis import sentiment_analyzer

# Initialize the Flask application
app = Flask(__name__)

# Route for rendering the HTML template
@app.route("/")
def render_index_page():
    return render_template('index.html')

# Route for handling the sentiment analysis
@app.route("/sentimentAnalyzer")
def sent_analyzer():
    # Retrieve the text to analyze from the request arguments (sent from JS)
    text_to_analyze = request.args.get('textToAnalyze')

    # Debugging: print the received text
    print(f"Received text to analyze: '{text_to_analyze}'")

    # Check if the text is not empty or just spaces
    if not text_to_analyze or text_to_analyze.strip() == '':
        return jsonify({"error": "Text is empty, please provide some text for sentiment analysis."}), 400
    
    # Call the sentiment analyzer function and get the response
    try:
        response = sentiment_analyzer(text_to_analyze)
        print(f"Response from sentiment analyzer: {response}")  # Debugging output

        # If the response contains an error, return it with status 422
        if 'error' in response:
            return jsonify(response), 422
        
        # Extract sentiment label and score
        label = response['label']
        score = response['score']
        
        # Format the result as JSON
        result = {
            'sentiment': {
                'label': label,
                'score': score
            }
        }
        
        return jsonify(result), 200

    except Exception as e:
        print(f"Error during sentiment analysis: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

# Run the application on localhost:5000
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
