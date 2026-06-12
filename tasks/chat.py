"""
Conversational Chat Task
"""
from typing import Dict, List
from utils.memory import ConversationMemory
import random


class ChatTask:
    """Conversational chatting module"""
    
    def __init__(self, memory: ConversationMemory):
        self.memory = memory
        self.responses = self._load_responses()
    
    @staticmethod
    def _load_responses() -> Dict[str, List[str]]:
        """Load pre-defined responses for common inputs"""
        return {
            "greeting": [
                "Hello! How can I help you today?",
                "Hi there! What's on your mind?",
                "Hey! Great to see you. What can I do for you?",
                "Welcome! I'm here to assist."
            ],
            "goodbye": [
                "Goodbye! Have a great day!",
                "See you later! Take care!",
                "Farewell! Feel free to come back anytime.",
                "Until next time!"
            ],
            "thanks": [
                "You're welcome!",
                "Happy to help!",
                "My pleasure!",
                "Anytime!"
            ],
            "joke": [
                "Why did the AI go to school? To improve its neural network!",
                "How many programmers does it take to change a light bulb? None, that's a hardware problem!",
                "Why do Java developers wear glasses? Because they don't C#!",
                "What do you call an AI that tells jokes? An algorithm of humor!"
            ],
            "default": [
                "That's interesting! Tell me more.",
                "I see. Can you elaborate on that?",
                "That sounds important. What else?",
                "I'm listening. Continue.",
                "Interesting perspective. How does that make you feel?"
            ]
        }
    
    def respond(self, user_input: str) -> str:
        """
        Generate conversational response
        
        Args:
            user_input: User's message
            
        Returns:
            Response from assistant
        """
        user_lower = user_input.lower()
        
        # Detect greeting
        greeting_words = ["hi", "hello", "hey", "greetings", "good morning", "good afternoon"]
        if any(word in user_lower for word in greeting_words):
            return random.choice(self.responses["greeting"])
        
        # Detect goodbye
        goodbye_words = ["bye", "goodbye", "farewell", "see you", "take care", "gotta go"]
        if any(word in user_lower for word in goodbye_words):
            return random.choice(self.responses["goodbye"])
        
        # Detect thanks
        thanks_words = ["thanks", "thank you", "appreciate", "grateful"]
        if any(word in user_lower for word in thanks_words):
            return random.choice(self.responses["thanks"])
        
        # Detect joke request
        joke_words = ["joke", "funny", "laugh", "make me laugh"]
        if any(word in user_lower for word in joke_words):
            return random.choice(self.responses["joke"])
        
        # Get context from memory
        context = self.memory.get_context(num_messages=3)
        
        # Generate contextual response
        response = self._generate_contextual_response(user_input, context)
        
        return response
    
    def _generate_contextual_response(self, user_input: str, context: str) -> str:
        """
        Generate contextual response based on memory
        
        Args:
            user_input: Current user input
            context: Recent conversation context
            
        Returns:
            Contextual response
        """
        # Simple contextual response generation
        response = random.choice(self.responses["default"])
        
        # Enhance with keywords from input
        words = user_input.split()
        if len(words) > 0:
            key_word = words[0] if len(words[0]) > 3 else words[-1] if words else "that"
            response = f"{response} You mentioned '{key_word}' - that's great!"
        
        return response
