import os
import re
import requests
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, EmotionOptions
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def is_valid_text(text):
    """
    Check if the text is valid for emotion analysis.
    - Text should not be too short.
    - Text should contain at least one alphabetic character.
    """
    if not text or len(text.strip()) < 1:  # Text too short
        return False
    if not re.search(r"[a-zA-Z]", text):  # No alphabetic characters found
        return False
    return True

def emotion_analyzer(text_to_analyse):
    try:
        # Validate input before making an API call
        if not is_valid_text(text_to_analyse):
            return {'error': 'Invalid text. Please enter valid text.', 'status_code': 422}

        # Load IBM Watson API credentials from environment variables
        api_key = os.getenv("IBM_API_KEY")
        url = os.getenv("IBM_API_URL")

        if not api_key or not url:
            return {'error': 'Missing API credentials. Please set them as environment variables.', 'status_code': 500}

        # Initialize Watson NLU
        authenticator = IAMAuthenticator(api_key)
        nlu = NaturalLanguageUnderstandingV1(
            version='2021-08-01',
            authenticator=authenticator
        )
        nlu.set_service_url(url)

        # Perform emotion analysis
        response = nlu.analyze(
            text=text_to_analyse,
            features=Features(emotion=EmotionOptions())
        )

        # Check status code
        if response.get_status_code() != 200:
            return {'error': 'Error from IBM Watson API.', 'status_code': response.get_status_code()}

        # Extract emotions
        result = response.get_result()
        emotions = result['emotion']['document']['emotion']

        # Determine dominant emotion
        dominant_emotion = max(emotions, key=emotions.get)

        # Format the response
        final_result = {
            'anger': emotions['anger'],
            'disgust': emotions['disgust'],
            'fear': emotions['fear'],
            'joy': emotions['joy'],
            'sadness': emotions['sadness'],
            'dominant_emotion': dominant_emotion,
            'status_code': 200
        }

        return final_result

    except requests.exceptions.RequestException:
        return {'error': 'Network error. Please check your internet connection.', 'status_code': 503}
    except Exception as e:
        return {'error': str(e), 'status_code': 500}
