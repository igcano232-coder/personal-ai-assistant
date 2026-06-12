"""
Tokenizer: Handles text preprocessing and tokenization
"""
import re
from typing import List, Dict
from config import TOKENIZER_CONFIG


class Tokenizer:
    """Simple tokenizer for text preprocessing"""
    
    def __init__(self, config: Dict = None):
        self.config = config or TOKENIZER_CONFIG
        self.stopwords = self._load_stopwords()
    
    @staticmethod
    def _load_stopwords() -> set:
        """Load common English stopwords"""
        common_stopwords = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'must', 'can', 'i', 'you', 'he', 'she',
            'it', 'we', 'they', 'what', 'which', 'who', 'when', 'where', 'why',
            'how', 'this', 'that', 'these', 'those', 'am', 'as', 'by', 'from',
            'up', 'about', 'into', 'through', 'during', 'before', 'after',
            'above', 'below', 'between', 'out', 'off', 'over', 'under', 'again',
            'further', 'then', 'once', 'here', 'there', 'all', 'both', 'each',
            'few', 'more', 'most', 'other', 'some', 'such', 'only', 'own',
            'same', 'so', 'than', 'too', 'very', 'just', 'no', 'not', 'nor',
            'such', 'if', 'because', 'while', 'own', 'does', 'your'
        }
        return common_stopwords
    
    def tokenize(self, text: str) -> List[str]:
        """
        Tokenize text into words
        
        Args:
            text: Input text to tokenize
            
        Returns:
            List of tokens
        """
        # Convert to lowercase if configured
        if self.config.get("lowercase", True):
            text = text.lower()
        
        # Remove punctuation if configured
        if self.config.get("remove_punctuation", True):
            text = re.sub(r'[^\w\s]', '', text)
        
        # Split into words
        tokens = text.split()
        
        # Remove stopwords if configured
        if self.config.get("remove_stopwords", False):
            tokens = [t for t in tokens if t not in self.stopwords]
        
        return tokens
    
    def preprocess(self, text: str) -> str:
        """
        Preprocess text without tokenization
        
        Args:
            text: Input text to preprocess
            
        Returns:
            Preprocessed text
        """
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Convert to lowercase if configured
        if self.config.get("lowercase", True):
            text = text.lower()
        
        return text
    
    def get_token_frequency(self, tokens: List[str]) -> Dict[str, int]:
        """
        Get frequency of each token
        
        Args:
            tokens: List of tokens
            
        Returns:
            Dictionary with token frequencies
        """
        freq = {}
        for token in tokens:
            freq[token] = freq.get(token, 0) + 1
        return freq
    
    def similarity_score(self, text1: str, text2: str) -> float:
        """
        Calculate simple similarity between two texts
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Similarity score (0-1)
        """
        tokens1 = set(self.tokenize(text1))
        tokens2 = set(self.tokenize(text2))
        
        if not tokens1 or not tokens2:
            return 0.0
        
        intersection = len(tokens1 & tokens2)
        union = len(tokens1 | tokens2)
        
        return intersection / union if union > 0 else 0.0
