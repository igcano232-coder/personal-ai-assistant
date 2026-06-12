"""
Question Answering Task
"""
from typing import Dict, List
from core.knowledge_base import KnowledgeBase


class QATask:
    """Question Answering module"""
    
    def __init__(self, knowledge_base: KnowledgeBase):
        self.kb = knowledge_base
        self.qa_patterns = self._load_qa_patterns()
    
    @staticmethod
    def _load_qa_patterns() -> Dict[str, str]:
        """Load common Q&A patterns"""
        return {
            "what is": "A {subject} is {definition}. It is commonly used for {application}.",
            "how to": "To {action}, follow these steps: 1. Prepare. 2. Execute. 3. Verify. 4. Optimize.",
            "why": "The reason is that {subject} has {property} which leads to {consequence}.",
            "when": "This typically occurs {timeframe} when {condition} is met.",
            "where": "You can find this in {location} or access it via {method}.",
            "who": "{entity} is a {role} known for {achievement}.",
        }
    
    def answer(self, question: str) -> str:
        """
        Generate answer to a question
        
        Args:
            question: The question to answer
            
        Returns:
            Answer to the question
        """
        # Search knowledge base
        similar = self.kb.search(question, top_k=3)
        
        if similar:
            # Return most similar answer
            best_match = similar[0]
            self.kb.update_access(best_match["query"])
            return best_match["response"]
        
        # Generate answer based on question type
        answer = self._generate_answer(question)
        
        return answer
    
    def _generate_answer(self, question: str) -> str:
        """
        Generate answer when no similar entry found
        
        Args:
            question: The question
            
        Returns:
            Generated answer
        """
        question_lower = question.lower()
        
        # Check question type
        for pattern, template in self.qa_patterns.items():
            if pattern in question_lower:
                # Extract subject from question
                subject = question.replace("What is", "").replace("what is", "").strip()
                
                # Simple answer generation
                if pattern == "what is":
                    return f"Based on my knowledge, {subject} is an important concept that many people find useful. Would you like more specific information about it?"
                elif pattern == "how to":
                    action = subject.replace("How to", "").replace("how to", "").strip()
                    return f"To {action}, I recommend: 1. Research thoroughly. 2. Plan your approach. 3. Take action step by step. 4. Review and improve."
                elif pattern == "why":
                    return f"That's an interesting question about {subject}. The reasons are usually multifaceted and depend on context."
        
        # Default answer
        return f"That's a great question about '{question}'. Let me learn more about this to give you a better answer next time."
    
    def add_qa_pair(self, question: str, answer: str) -> None:
        """
        Add a Q&A pair to knowledge base
        
        Args:
            question: Question
            answer: Answer
        """
        self.kb.add_entry(question, answer, category="qa")
