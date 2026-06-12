"""
Knowledge Base: Stores and retrieves information
"""
from typing import List, Dict, Optional
from datetime import datetime
from .tokenizer import Tokenizer
from config import KB_CONFIG


class KnowledgeEntry:
    """Represents a single knowledge entry"""
    
    def __init__(self, query: str, response: str, category: str = "general"):
        self.query = query
        self.response = response
        self.category = category
        self.created_at = datetime.now()
        self.access_count = 0
        self.last_accessed = datetime.now()
    
    def to_dict(self) -> Dict:
        return {
            "query": self.query,
            "response": self.response,
            "category": self.category,
            "created_at": self.created_at.isoformat(),
            "access_count": self.access_count,
            "last_accessed": self.last_accessed.isoformat()
        }


class KnowledgeBase:
    """Manages knowledge storage and retrieval"""
    
    def __init__(self, config: Dict = None):
        self.config = config or KB_CONFIG
        self.entries: List[KnowledgeEntry] = []
        self.tokenizer = Tokenizer()
        self.categories = set()
    
    def add_entry(self, query: str, response: str, category: str = "general") -> None:
        """
        Add a new knowledge entry
        
        Args:
            query: Question or input
            response: Answer or output
            category: Category of knowledge
        """
        if len(self.entries) >= self.config.get("max_knowledge_entries", 1000):
            # Remove oldest entry if limit reached
            self.entries.pop(0)
        
        entry = KnowledgeEntry(query, response, category)
        self.entries.append(entry)
        self.categories.add(category)
    
    def search(self, query: str, top_k: int = 5, threshold: float = None) -> List[Dict]:
        """
        Search for similar entries in knowledge base
        
        Args:
            query: Search query
            top_k: Number of top results to return
            threshold: Minimum similarity threshold
            
        Returns:
            List of similar entries with similarity scores
        """
        if threshold is None:
            threshold = self.config.get("similarity_threshold", 0.6)
        
        results = []
        
        for entry in self.entries:
            similarity = self.tokenizer.similarity_score(query, entry.query)
            
            if similarity >= threshold:
                results.append({
                    "query": entry.query,
                    "response": entry.response,
                    "category": entry.category,
                    "similarity": similarity,
                    "access_count": entry.access_count
                })
        
        # Sort by similarity (descending) and then by access count (descending)
        results.sort(key=lambda x: (x["similarity"], x["access_count"]), reverse=True)
        
        return results[:top_k]
    
    def get_by_category(self, category: str) -> List[Dict]:
        """
        Get all entries in a specific category
        
        Args:
            category: Category name
            
        Returns:
            List of entries in the category
        """
        return [
            entry.to_dict()
            for entry in self.entries
            if entry.category == category
        ]
    
    def update_access(self, query: str) -> None:
        """
        Update access statistics for a query
        
        Args:
            query: Query to update
        """
        for entry in self.entries:
            if entry.query.lower() == query.lower():
                entry.access_count += 1
                entry.last_accessed = datetime.now()
                break
    
    def clear(self) -> None:
        """Clear all entries"""
        self.entries.clear()
        self.categories.clear()
    
    def get_stats(self) -> Dict:
        """
        Get statistics about the knowledge base
        
        Returns:
            Dictionary with KB statistics
        """
        total_accesses = sum(e.access_count for e in self.entries)
        
        return {
            "total_entries": len(self.entries),
            "categories": len(self.categories),
            "total_accesses": total_accesses,
            "avg_accesses_per_entry": total_accesses / len(self.entries) if self.entries else 0,
            "categories_list": list(self.categories)
        }
