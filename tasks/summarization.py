"""
Text Summarization Task
"""
from typing import List
import re


class SummarizationTask:
    """Text summarization module"""
    
    def __init__(self, ratio: float = 0.3):
        """
        Initialize summarization task
        
        Args:
            ratio: Compression ratio (0.0 to 1.0)
        """
        self.ratio = ratio
    
    def summarize(self, text: str, num_sentences: int = None) -> str:
        """
        Summarize text using extractive summarization
        
        Args:
            text: Text to summarize
            num_sentences: Number of sentences in summary (if None, uses ratio)
            
        Returns:
            Summarized text
        """
        # Split into sentences
        sentences = self._split_sentences(text)
        
        if len(sentences) <= 2:
            return text
        
        # Determine number of summary sentences
        if num_sentences is None:
            num_sentences = max(1, int(len(sentences) * self.ratio))
        
        # Score sentences
        scores = self._score_sentences(sentences)
        
        # Get top sentences
        ranked = sorted(
            [(i, sent, scores[i]) for i, sent in enumerate(sentences)],
            key=lambda x: x[2],
            reverse=True
        )[:num_sentences]
        
        # Sort by original order
        summary_sentences = sorted(ranked, key=lambda x: x[0])
        
        # Join sentences
        summary = " ".join([sent for _, sent, _ in summary_sentences])
        
        return summary
    
    def _split_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences
        
        Args:
            text: Input text
            
        Returns:
            List of sentences
        """
        # Simple sentence splitting
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        return sentences
    
    def _score_sentences(self, sentences: List[str]) -> List[float]:
        """
        Score sentences based on keyword frequency
        
        Args:
            sentences: List of sentences
            
        Returns:
            List of scores
        """
        scores = []
        
        # Get word frequencies
        words = {}
        for sentence in sentences:
            for word in sentence.lower().split():
                # Remove punctuation
                word = re.sub(r'[^a-z0-9]', '', word)
                if len(word) > 3:  # Only consider words longer than 3 chars
                    words[word] = words.get(word, 0) + 1
        
        # Score sentences
        for sentence in sentences:
            score = 0
            for word in sentence.lower().split():
                word = re.sub(r'[^a-z0-9]', '', word)
                score += words.get(word, 0)
            
            # Normalize by sentence length
            avg_score = score / len(sentence.split()) if sentence.split() else 0
            scores.append(avg_score)
        
        return scores
