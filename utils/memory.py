"""
Conversation Memory: Maintains conversation history
"""
from typing import List, Dict, Optional
from datetime import datetime
from collections import deque


class Message:
    """Represents a single message in conversation"""
    
    def __init__(self, content: str, sender: str = "user", timestamp: datetime = None):
        self.content = content
        self.sender = sender  # "user" or "assistant"
        self.timestamp = timestamp or datetime.now()
    
    def to_dict(self) -> Dict:
        return {
            "content": self.content,
            "sender": self.sender,
            "timestamp": self.timestamp.isoformat()
        }


class ConversationMemory:
    """Manages conversation history with limited memory"""
    
    def __init__(self, max_size: int = 50):
        self.max_size = max_size
        self.history: deque = deque(maxlen=max_size)
        self.turn_count = 0
    
    def add_user_message(self, content: str) -> None:
        """
        Add user message to memory
        
        Args:
            content: Message content
        """
        message = Message(content, sender="user")
        self.history.append(message)
        self.turn_count += 1
    
    def add_assistant_message(self, content: str) -> None:
        """
        Add assistant message to memory
        
        Args:
            content: Message content
        """
        message = Message(content, sender="assistant")
        self.history.append(message)
    
    def get_context(self, num_messages: int = 5) -> str:
        """
        Get recent conversation context
        
        Args:
            num_messages: Number of recent messages to include
            
        Returns:
            Formatted conversation context
        """
        recent = list(self.history)[-num_messages:]
        context = ""
        
        for message in recent:
            sender = "You" if message.sender == "user" else "Assistant"
            context += f"{sender}: {message.content}\n"
        
        return context.strip()
    
    def get_history(self) -> List[Dict]:
        """
        Get full conversation history
        
        Returns:
            List of message dictionaries
        """
        return [msg.to_dict() for msg in self.history]
    
    def clear(self) -> None:
        """Clear conversation history"""
        self.history.clear()
        self.turn_count = 0
    
    def get_last_user_message(self) -> Optional[str]:
        """
        Get the last user message
        
        Returns:
            Last user message or None
        """
        for message in reversed(self.history):
            if message.sender == "user":
                return message.content
        return None
    
    def get_summary(self) -> Dict:
        """
        Get conversation summary
        
        Returns:
            Dictionary with conversation stats
        """
        user_msgs = [m for m in self.history if m.sender == "user"]
        assistant_msgs = [m for m in self.history if m.sender == "assistant"]
        
        return {
            "total_messages": len(self.history),
            "user_messages": len(user_msgs),
            "assistant_messages": len(assistant_msgs),
            "turns": self.turn_count,
            "first_message": self.history[0].timestamp.isoformat() if self.history else None,
            "last_message": self.history[-1].timestamp.isoformat() if self.history else None
        }
