import re
import requests
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def is_valid_text(text):
    """
    Check if the text is valid for sentiment analysis.
    - Text should not be too short.
    - Text should contain at least one alphabetic character.
    """
    if not text or len(text.strip()) < 1:  # Text too short
        return False
    if not re.search(r"[a-zA-Z]", text):  # No alphabetic characters found
        return False
    return True

def sentiment_analyzer(text_to_analyse):
    try:
        # Validate input before making an API call
        if not is_valid_text(text_to_analyse):
            return {'error': 'Invalid text. Please enter valid text.'}

        # Load IBM Watson API credentials from environment variables
        api_key = os.getenv("IBM_API_KEY")
        url = os.getenv("IBM_API_URL")

        if not api_key or not url:
            return {'error': 'Missing API credentials. Please set them as environment variables.'}

        # Initialize Watson NLU
        authenticator = IAMAuthenticator(api_key)
        nlu = NaturalLanguageUnderstandingV1(
            version='2021-08-01',
            authenticator=authenticator
        )
        nlu.set_service_url(url)

        # Perform sentiment analysis
        response = nlu.analyze(
            text=text_to_analyse,
            features=Features(sentiment=SentimentOptions())
        )

        # Check if the response is not 200 (error case)
        if response.get_status_code() != 200:
            return {'error': 'Invalid text. Please enter valid text.'}

        # Extract sentiment label and score
        result = response.get_result()
        label = result['sentiment']['document']['label']
        score = result['sentiment']['document']['score']

        return {'label': label, 'score': score}

    except requests.exceptions.RequestException:
        return {'error': 'Network error. Please check your internet connection.'}
    except Exception as e:
        return {'error': 'Invalid text. Please enter valid text.'}
