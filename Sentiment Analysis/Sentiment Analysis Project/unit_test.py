import unittest
from SentimentAnalysis.sentiment_analysis import sentiment_analyzer

class TestSentimentAnalyzer(unittest.TestCase):
    def test_sentiment_analyzer(self):
        # Test case for positive sentiment
        result_1 = sentiment_analyzer('I love working with Python')
        self.assertEqual(result_1['label'], 'positive')  # Updated expected output

        # Test case for negative sentiment
        result_2 = sentiment_analyzer('I hate working with Python')
        self.assertEqual(result_2['label'], 'negative')  # Updated expected output

        # Test case for neutral sentiment
        result_3 = sentiment_analyzer('I am neutral on Python')
        self.assertEqual(result_3['label'], 'neutral')  # Updated expected output

if __name__ == '__main__':
    unittest.main()
