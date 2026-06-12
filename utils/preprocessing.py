"""
Text Preprocessing Utilities
"""
import re
from typing import List, Set


def preprocess_text(text: str) -> str:
    """
    Preprocess text for analysis
    
    Args:
        text: Raw text
        
    Returns:
        Cleaned text
    """
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)
    
    # Remove special characters but keep spaces and punctuation
    text = re.sub(r'[^a-zA-Z0-9\s\.!?]', '', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text


def extract_keywords(text: str, top_n: int = 5) -> List[str]:
    """
    Extract key words from text (simple frequency-based)
    
    Args:
        text: Input text
        top_n: Number of keywords to extract
        
    Returns:
        List of keywords
    """
    # Preprocess
    text = preprocess_text(text).lower()
    
    # Stopwords to exclude
    stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                 'of', 'with', 'is', 'are', 'as', 'by', 'from', 'up', 'about', 'into'}
    
    # Get words
    words = text.split()
    
    # Filter stopwords and short words
    keywords = [w for w in words if w not in stopwords and len(w) > 2]
    
    # Count frequencies
    freq = {}
    for word in keywords:
        freq[word] = freq.get(word, 0) + 1
    
    # Sort by frequency
    sorted_keywords = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    
    return [word for word, _ in sorted_keywords[:top_n]]


def count_sentences(text: str) -> int:
    """
    Count sentences in text
    
    Args:
        text: Input text
        
    Returns:
        Number of sentences
    """
    return len(re.split(r'[.!?]+', text.strip())) - 1


def truncate_text(text: str, max_length: int = 100) -> str:
    """
    Truncate text to maximum length
    
    Args:
        text: Input text
        max_length: Maximum length
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."
