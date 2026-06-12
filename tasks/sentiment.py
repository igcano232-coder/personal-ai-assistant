"""
Sentiment Analysis Task
"""
from typing import Dict, Tuple


class SentimentTask:
    """Sentiment analysis module"""
    
    def __init__(self):
        self.positive_words = self._load_positive_words()
        self.negative_words = self._load_negative_words()
    
    @staticmethod
    def _load_positive_words() -> set:
        """Load positive sentiment words"""
        return {
            'good', 'great', 'amazing', 'awesome', 'excellent', 'wonderful', 'fantastic',
            'brilliant', 'outstanding', 'perfect', 'love', 'like', 'happy', 'joy', 'pleased',
            'delighted', 'thrilled', 'best', 'better', 'beautiful', 'lovely', 'nice', 'fine',
            'decent', 'cool', 'neat', 'glad', 'wonderful', 'superb', 'magnificent', 'splendid',
            'favorable', 'positive', 'success', 'achievement', 'win', 'victory'
        }
    
    @staticmethod
    def _load_negative_words() -> set:
        """Load negative sentiment words"""
        return {
            'bad', 'terrible', 'awful', 'horrible', 'hate', 'dislike', 'sad', 'angry',
            'disappointed', 'upset', 'angry', 'furious', 'worst', 'worse', 'ugly', 'disgusting',
            'gross', 'yuck', 'ugh', 'depressed', 'miserable', 'wretched', 'pathetic', 'useless',
            'worthless', 'failure', 'disaster', 'catastrophe', 'ruin', 'destroyed', 'broken',
            'negative', 'unfavorable', 'poor', 'weak', 'sick', 'ill', 'annoyed', 'irritated'
        }
    
    def analyze(self, text: str) -> str:
        """
        Analyze sentiment of text
        
        Args:
            text: Text to analyze
            
        Returns:
            Sentiment label: 'positive', 'negative', or 'neutral'
        """
        score, confidence = self._calculate_sentiment_score(text)
        
        if score > 0.1:
            return "positive"
        elif score < -0.1:
            return "negative"
        else:
            return "neutral"
    
    def _calculate_sentiment_score(self, text: str) -> Tuple[float, float]:
        """
        Calculate sentiment score
        
        Args:
            text: Text to analyze
            
        Returns:
            Tuple of (score, confidence)
        """
        words = text.lower().split()
        
        positive_count = sum(1 for word in words if word in self.positive_words)
        negative_count = sum(1 for word in words if word in self.negative_words)
        total_sentiment_words = positive_count + negative_count
        
        if total_sentiment_words == 0:
            return 0.0, 0.0
        
        # Calculate score: +1 to -1
        score = (positive_count - negative_count) / total_sentiment_words
        
        # Calculate confidence
        confidence = total_sentiment_words / len(words) if words else 0
        
        return score, confidence
    
    def get_sentiment_details(self, text: str) -> Dict:
        """
        Get detailed sentiment analysis
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with detailed sentiment info
        """
        score, confidence = self._calculate_sentiment_score(text)
        sentiment = self.analyze(text)
        
        words = text.lower().split()
        positive_found = [w for w in words if w in self.positive_words]
        negative_found = [w for w in words if w in self.negative_words]
        
        return {
            "sentiment": sentiment,
            "score": score,
            "confidence": confidence,
            "positive_words": positive_found,
            "negative_words": negative_found
        }
