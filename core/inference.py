"""
Inference Engine: Main AI logic and task routing
"""
from typing import Dict, Optional
from .tokenizer import Tokenizer
from .knowledge_base import KnowledgeBase
from utils.memory import ConversationMemory
from tasks.qa import QATask
from tasks.chat import ChatTask
from tasks.sentiment import SentimentTask
from tasks.summarization import SummarizationTask
from config import MODEL_CONFIG, DEBUG


class AIAssistant:
    """Main AI Assistant that coordinates all tasks"""
    
    def __init__(self):
        self.tokenizer = Tokenizer()
        self.knowledge_base = KnowledgeBase()
        self.memory = ConversationMemory(max_size=MODEL_CONFIG.get("memory_size", 50))
        
        # Initialize all task modules
        self.qa_task = QATask(self.knowledge_base)
        self.chat_task = ChatTask(self.memory)
        self.sentiment_task = SentimentTask()
        self.summarization_task = SummarizationTask()
        
        self.debug = DEBUG
    
    def process(self, user_input: str) -> Dict:
        """
        Main processing pipeline for user input
        
        Args:
            user_input: User's input text
            
        Returns:
            Dictionary with response and metadata
        """
        # Preprocess input
        preprocessed = self.tokenizer.preprocess(user_input)
        
        # Add to memory
        self.memory.add_user_message(preprocessed)
        
        # Detect task and get response
        response = self._route_task(preprocessed)
        
        # Add response to memory
        self.memory.add_assistant_message(response["response"])
        
        # Store in knowledge base
        self.knowledge_base.add_entry(preprocessed, response["response"], response["task"])
        
        return {
            "response": response["response"],
            "task": response["task"],
            "confidence": response.get("confidence", 1.0),
            "metadata": response.get("metadata", {})
        }
    
    def _route_task(self, user_input: str) -> Dict:
        """
        Route input to appropriate task module
        
        Args:
            user_input: Processed user input
            
        Returns:
            Task response dictionary
        """
        # Get sentiment analysis
        sentiment = self.sentiment_task.analyze(user_input)
        
        # Check if it's a summarization request
        if any(word in user_input.lower() for word in ["summarize", "summary", "brief", "condense"]):
            return {
                "response": self.summarization_task.summarize(user_input),
                "task": "summarization",
                "metadata": {"sentiment": sentiment}
            }
        
        # Check if it's a question
        if self._is_question(user_input):
            qa_response = self.qa_task.answer(user_input)
            return {
                "response": qa_response,
                "task": "qa",
                "metadata": {"sentiment": sentiment}
            }
        
        # Default to chat
        chat_response = self.chat_task.respond(user_input)
        return {
            "response": chat_response,
            "task": "chat",
            "metadata": {"sentiment": sentiment}
        }
    
    def _is_question(self, text: str) -> bool:
        """Check if text is a question"""
        question_indicators = ["what", "how", "why", "when", "where", "who", "which", "?"]
        text_lower = text.lower()
        return any(indicator in text_lower for indicator in question_indicators)
    
    def ask(self, question: str) -> str:
        """Ask a question"""
        result = self.process(question)
        return result["response"]
    
    def chat(self, message: str) -> str:
        """Chat with the assistant"""
        result = self.process(message)
        return result["response"]
    
    def analyze_sentiment(self, text: str) -> str:
        """Analyze sentiment of text"""
        return self.sentiment_task.analyze(text)
    
    def summarize(self, text: str) -> str:
        """Summarize text"""
        return self.summarization_task.summarize(text)
    
    def get_stats(self) -> Dict:
        """Get assistant statistics"""
        return {
            "knowledge_base": self.knowledge_base.get_stats(),
            "memory_size": len(self.memory.history),
            "total_interactions": self.memory.turn_count
        }
    
    def reset_memory(self) -> None:
        """Reset conversation memory"""
        self.memory.clear()
    
    def _debug_print(self, message: str) -> None:
        """Print debug messages if enabled"""
        if self.debug:
            print(f"[DEBUG] {message}")
