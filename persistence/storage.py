"""
Persistent Storage: Handles all data persistence operations
"""
import json
import os
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path
import shutil
from config import STORAGE_CONFIG


class PersistentStorage:
    """Manages all persistent storage operations"""
    
    def __init__(self):
        self.config = STORAGE_CONFIG
        self.data_dir = Path(self.config.get("data_dir", "data"))
        self.storage_type = self.config.get("storage_type", "json")
        
        # Create data directories
        self._setup_directories()
    
    def _setup_directories(self) -> None:
        """Create necessary directories"""
        directories = [
            self.data_dir,
            self.data_dir / "memories",
            self.data_dir / "conversations",
            self.data_dir / "knowledge_base",
            self.data_dir / "backups",
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def save_conversation(self, session_id: str, messages: List[Dict]) -> bool:
        """
        Save entire conversation to disk
        
        Args:
            session_id: Unique session identifier
            messages: List of message dictionaries
            
        Returns:
            Success status
        """
        try:
            filepath = self.data_dir / "conversations" / f"{session_id}.json"
            
            data = {
                "session_id": session_id,
                "created_at": datetime.now().isoformat(),
                "message_count": len(messages),
                "messages": messages
            }
            
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error saving conversation: {e}")
            return False
    
    def load_conversation(self, session_id: str) -> Optional[List[Dict]]:
        """
        Load conversation from disk
        
        Args:
            session_id: Session identifier
            
        Returns:
            List of messages or None if not found
        """
        try:
            filepath = self.data_dir / "conversations" / f"{session_id}.json"
            
            if not filepath.exists():
                return None
            
            with open(filepath, 'r') as f:
                data = json.load(f)
                return data.get("messages", [])
        except Exception as e:
            print(f"Error loading conversation: {e}")
            return None
    
    def save_memory(self, memory_entry: Dict) -> bool:
        """
        Save individual memory entry
        
        Args:
            memory_entry: Memory entry dictionary
            
        Returns:
            Success status
        """
        try:
            memory_id = memory_entry.get("id", datetime.now().timestamp())
            filepath = self.data_dir / "memories" / f"{memory_id}.json"
            
            memory_entry["saved_at"] = datetime.now().isoformat()
            
            with open(filepath, 'w') as f:
                json.dump(memory_entry, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error saving memory: {e}")
            return False
    
    def load_all_memories(self) -> List[Dict]:
        """
        Load all memories from disk
        
        Returns:
            List of all memory entries
        """
        try:
            memories = []
            memories_dir = self.data_dir / "memories"
            
            if not memories_dir.exists():
                return memories
            
            for filepath in sorted(memories_dir.glob("*.json")):
                with open(filepath, 'r') as f:
                    memory = json.load(f)
                    memories.append(memory)
            
            return memories
        except Exception as e:
            print(f"Error loading memories: {e}")
            return []
    
    def save_knowledge_base(self, kb_entries: List[Dict]) -> bool:
        """
        Save knowledge base to disk
        
        Args:
            kb_entries: Knowledge base entries
            
        Returns:
            Success status
        """
        try:
            filepath = self.data_dir / "knowledge_base" / "kb.json"
            
            data = {
                "saved_at": datetime.now().isoformat(),
                "entry_count": len(kb_entries),
                "entries": kb_entries
            }
            
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error saving knowledge base: {e}")
            return False
    
    def load_knowledge_base(self) -> List[Dict]:
        """
        Load knowledge base from disk
        
        Returns:
            List of KB entries
        """
        try:
            filepath = self.data_dir / "knowledge_base" / "kb.json"
            
            if not filepath.exists():
                return []
            
            with open(filepath, 'r') as f:
                data = json.load(f)
                return data.get("entries", [])
        except Exception as e:
            print(f"Error loading knowledge base: {e}")
            return []
    
    def create_backup(self) -> bool:
        """
        Create backup of all data
        
        Returns:
            Success status
        """
        try:
            backups_dir = self.data_dir / "backups"
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = backups_dir / f"backup_{timestamp}"
            
            # Copy data directory to backup
            src_dirs = [
                self.data_dir / "memories",
                self.data_dir / "conversations",
                self.data_dir / "knowledge_base"
            ]
            
            for src_dir in src_dirs:
                if src_dir.exists():
                    dst_dir = backup_path / src_dir.name
                    shutil.copytree(src_dir, dst_dir, dirs_exist_ok=True)
            
            # Clean old backups
            self._cleanup_old_backups()
            
            return True
        except Exception as e:
            print(f"Error creating backup: {e}")
            return False
    
    def _cleanup_old_backups(self) -> None:
        """
        Keep only the N most recent backups
        """
        try:
            backups_dir = self.data_dir / "backups"
            max_backups = self.config.get("backup_count", 3)
            
            if not backups_dir.exists():
                return
            
            backup_dirs = sorted(backups_dir.glob("backup_*"), reverse=True)
            
            for backup_dir in backup_dirs[max_backups:]:
                shutil.rmtree(backup_dir)
        except Exception as e:
            print(f"Error cleaning backups: {e}")
    
    def export_data(self, export_path: str) -> bool:
        """
        Export all data to a zip file
        
        Args:
            export_path: Path to export file
            
        Returns:
            Success status
        """
        try:
            shutil.make_archive(export_path, 'zip', self.data_dir)
            return True
        except Exception as e:
            print(f"Error exporting data: {e}")
            return False
    
    def get_statistics(self) -> Dict:
        """
        Get storage statistics
        
        Returns:
            Dictionary with storage stats
        """
        memories = self.load_all_memories()
        kb_entries = self.load_knowledge_base()
        
        # Count conversations
        conversations_dir = self.data_dir / "conversations"
        conversation_count = len(list(conversations_dir.glob("*.json"))) if conversations_dir.exists() else 0
        
        # Get directory sizes
        def get_dir_size(path):
            if not path.exists():
                return 0
            return sum(f.stat().st_size for f in path.rglob('*') if f.is_file())
        
        return {
            "total_memories": len(memories),
            "total_kb_entries": len(kb_entries),
            "total_conversations": conversation_count,
            "memories_size_mb": round(get_dir_size(self.data_dir / "memories") / 1024 / 1024, 2),
            "conversations_size_mb": round(get_dir_size(self.data_dir / "conversations") / 1024 / 1024, 2),
            "total_size_mb": round(get_dir_size(self.data_dir) / 1024 / 1024, 2),
        }
    
    def delete_old_memories(self, days: int = 30) -> int:
        """
        Delete memories older than N days
        
        Args:
            days: Number of days to keep
            
        Returns:
            Number of deleted memories
        """
        try:
            deleted_count = 0
            cutoff_date = datetime.now().timestamp() - (days * 86400)
            memories_dir = self.data_dir / "memories"
            
            if not memories_dir.exists():
                return 0
            
            for filepath in memories_dir.glob("*.json"):
                if filepath.stat().st_mtime < cutoff_date:
                    filepath.unlink()
                    deleted_count += 1
            
            return deleted_count
        except Exception as e:
            print(f"Error deleting old memories: {e}")
            return 0
