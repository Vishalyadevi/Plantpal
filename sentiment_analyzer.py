from textblob import TextBlob
import nltk

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/brown')
except LookupError:
    nltk.download('brown')

class SentimentAnalyzer:
    @staticmethod
    def analyze(text):
        """
        Analyze sentiment of text and return score and label
        Returns: dict with 'score' (float -1 to 1) and 'label' (str)
        """
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        
        # Determine sentiment label
        if polarity > 0.1:
            label = 'positive'
            growth_points = 20
        elif polarity < -0.1:
            label = 'negative'
            growth_points = 0
        else:
            label = 'neutral'
            growth_points = 5
        
        return {
            'score': polarity,
            'label': label,
            'growth_points': growth_points,
            'subjectivity': blob.sentiment.subjectivity
        }
    
    @staticmethod
    def get_emoji(label):
        """Return emoji based on sentiment label"""
        emojis = {
            'positive': '😊',
            'neutral': '😐',
            'negative': '😔'
        }
        return emojis.get(label, '😐')
    
    @staticmethod
    def get_plant_state(label):
        """Return plant animation state based on sentiment"""
        states = {
            'positive': 'growing',
            'neutral': 'idle',
            'negative': 'calming'
        }
        return states.get(label, 'idle')