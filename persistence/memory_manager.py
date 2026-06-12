"""
Memory Manager: Advanced memory management and recall system
"""
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from core.tokenizer import Tokenizer
from .storage import PersistentStorage
from config import STORAGE_CONFIG


class Memory:
    """Represents a single memory entry"""
    
    def __init__(self, content: str, memory_type: str = "interaction", 
                 context: Dict = None, tags: List[str] = None):
        self.id = datetime.now().timestamp()
        self.content = content
        self.memory_type = memory_type  # interaction, learning, user_profile, etc
        self.context = context or {}
        self.tags = tags or []
        self.created_at = datetime.now()
        self.access_count = 0
        self.last_accessed = datetime.now()
        self.importance = 1.0  # 0.0 to 1.0
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "content": self.content,
            "type": self.memory_type,
            "context": self.context,
            "tags": self.tags,
            "created_at": self.created_at.isoformat(),
            "access_count": self.access_count,
            "last_accessed": self.last_accessed.isoformat(),
            "importance": self.importance
        }


class MemoryManager:
    """Manages persistent memory system"""
    
    def __init__(self):
        self.storage = PersistentStorage()
        self.tokenizer = Tokenizer()
        self.memories: List[Memory] = []
        self.session_memories: List[Memory] = []  # Current session
        self.save_counter = 0
        self.save_interval = STORAGE_CONFIG.get("save_interval", 5)
        
        # Load existing memories
        self._load_memories()
    
    def _load_memories(self) -> None:
        """
        Load all persisted memories from storage
        """
        try:
            memory_dicts = self.storage.load_all_memories()
            self.memories = []
            
            for mem_dict in memory_dicts:
                memory = Memory(
                    content=mem_dict.get("content", ""),
                    memory_type=mem_dict.get("type", "interaction"),
                    context=mem_dict.get("context", {}),
                    tags=mem_dict.get("tags", [])
                )
                memory.id = mem_dict.get("id", memory.id)
                memory.access_count = mem_dict.get("access_count", 0)
                memory.importance = mem_dict.get("importance", 1.0)
                self.memories.append(memory)
        except Exception as e:
            print(f"Error loading memories: {e}")
    
    def add_memory(self, content: str, memory_type: str = "interaction",
                   context: Dict = None, tags: List[str] = None,
                   importance: float = 1.0) -> Memory:
        """
        Add a new memory
        
        Args:
            content: Memory content
            memory_type: Type of memory
            context: Additional context
            tags: Memory tags
            importance: Importance score (0-1)
            
        Returns:
            Created Memory object
        """
        memory = Memory(content, memory_type, context, tags)
        memory.importance = max(0.0, min(1.0, importance))
        
        self.memories.append(memory)
        self.session_memories.append(memory)
        
        # Auto-save if interval reached
        self.save_counter += 1
        if self.save_counter >= self.save_interval:
            self.save_memories()
            self.save_counter = 0
        
        return memory
    
    def save_memories(self) -> bool:
        """
        Save all memories to persistent storage
        
        Returns:
            Success status
        """
        try:
            max_entries = STORAGE_CONFIG.get("max_memory_entries", 10000)
            
            # Keep only most important memories if over limit
            if len(self.memories) > max_entries:
                self.memories.sort(key=lambda m: m.importance, reverse=True)
                self.memories = self.memories[:max_entries]
            
            for memory in self.memories:
                self.storage.save_memory(memory.to_dict())
            
            return True
        except Exception as e:
            print(f"Error saving memories: {e}")
            return False
    
    def recall(self, query: str, top_k: int = 5, 
               memory_type: Optional[str] = None) -> List[Dict]:
        """
        Recall memories similar to query
        
        Args:
            query: Search query
            top_k: Number of results to return
            memory_type: Filter by memory type
            
        Returns:
            List of similar memories
        """
        results = []
        
        for memory in self.memories:
            # Filter by type if specified
            if memory_type and memory.memory_type != memory_type:
                continue
            
            # Calculate similarity
            similarity = self.tokenizer.similarity_score(query, memory.content)
            
            if similarity > 0.3:  # Minimum similarity threshold
                results.append({
                    "content": memory.content,
                    "type": memory.memory_type,
                    "context": memory.context,
                    "tags": memory.tags,
                    "similarity": similarity,
                    "importance": memory.importance,
                    "access_count": memory.access_count,
                    "created_at": memory.created_at.isoformat(),
                    "age_days": (datetime.now() - memory.created_at).days
                })
        
        # Sort by similarity and importance
        results.sort(key=lambda x: (x["similarity"], x["importance"], x["access_count"]), reverse=True)
        
        return results[:top_k]
    
    def search_by_tag(self, tag: str, top_k: int = 10) -> List[Dict]:
        """
        Search memories by tag
        
        Args:
            tag: Tag to search for
            top_k: Number of results
            
        Returns:
            List of memories with the tag
        """
        results = []
        
        for memory in self.memories:
            if tag.lower() in [t.lower() for t in memory.tags]:
                results.append({
                    "content": memory.content,
                    "type": memory.memory_type,
                    "tags": memory.tags,
                    "importance": memory.importance,
                    "created_at": memory.created_at.isoformat()
                })
        
        # Sort by importance and recency
        results.sort(key=lambda x: (x["importance"], x["created_at"]), reverse=True)
        
        return results[:top_k]
    
    def search_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Dict]:
        """
        Search memories by date range
        
        Args:
            start_date: Start date
            end_date: End date
            
        Returns:
            List of memories in date range
        """
        results = []
        
        for memory in self.memories:
            if start_date <= memory.created_at <= end_date:
                results.append({
                    "content": memory.content,
                    "type": memory.memory_type,
                    "created_at": memory.created_at.isoformat(),
                    "importance": memory.importance
                })
        
        results.sort(key=lambda x: x["created_at"], reverse=True)
        return results
    
    def update_access(self, memory_id: float) -> None:
        """
        Update access statistics for a memory
        
        Args:
            memory_id: Memory identifier
        """
        for memory in self.memories:
            if memory.id == memory_id:
                memory.access_count += 1
                memory.last_accessed = datetime.now()
                break
    
    def get_user_profile(self) -> Dict:
        """
        Build user profile from memories
        
        Returns:
            User profile dictionary
        """
        profile_memories = [m for m in self.memories if m.memory_type == "user_profile"]
        
        profile = {
            "preferences": {},
            "habits": {},
            "interests": [],
            "learned_information": []
        }
        
        for memory in profile_memories:
            if "preference" in memory.tags:
                profile["preferences"].update(memory.context)
            elif "habit" in memory.tags:
                profile["habits"].update(memory.context)
            elif "interest" in memory.tags:
                profile["interests"].append(memory.content)
            elif "learning" in memory.tags:
                profile["learned_information"].append(memory.content)
        
        return profile
    
    def get_statistics(self) -> Dict:
        """
        Get memory system statistics
        
        Returns:
            Statistics dictionary
        """
        memory_types = {}
        total_importance = 0
        
        for memory in self.memories:
            memory_types[memory.memory_type] = memory_types.get(memory.memory_type, 0) + 1
            total_importance += memory.importance
        
        return {
            "total_memories": len(self.memories),
            "session_memories": len(self.session_memories),
            "memory_types": memory_types,
            "avg_importance": total_importance / len(self.memories) if self.memories else 0,
            "total_accesses": sum(m.access_count for m in self.memories),
            "avg_age_days": sum((datetime.now() - m.created_at).days for m in self.memories) / len(self.memories) if self.memories else 0,
            "storage": self.storage.get_statistics()
        }
    
    def clear_session_memory(self) -> None:
        """
        Clear current session memory
        """
        self.session_memories.clear()
    
    def export_memories(self, export_path: str) -> bool:
        """
        Export all memories
        
        Args:
            export_path: Path to export to
            
        Returns:
            Success status
        """
        return self.storage.export_data(export_path)
