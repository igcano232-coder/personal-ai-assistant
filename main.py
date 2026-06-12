#!/usr/bin/env python3
"""
Main Entry Point: Personal AI Assistant CLI with Persistent Memory
"""
import sys
from core.inference import AIAssistant
from config import DEBUG, VERBOSE
from datetime import datetime, timedelta


def print_welcome():
    """Print welcome message"""
    print("\n" + "="*60)
    print("🤖 Personal AI Assistant v2.0")
    print("Built from scratch, no external APIs required")
    print("WITH PERSISTENT MEMORY 💾")
    print("="*60)
    print("\nCommands:")
    print("  /help           - Show help menu")
    print("  /stats          - Show AI statistics")
    print("  /memory         - Show conversation memory")
    print("  /recall [query] - Recall memories by query")
    print("  /search [tag]   - Search memories by tag")
    print("  /profile        - Show user profile")
    print("  /clear          - Clear session memory (keeps persistent)")
    print("  /save           - Force save all data")
    print("  /export [path]  - Export all data to zip")
    print("  /exit           - Exit the assistant")
    print("\nOtherwise, just type your message and I'll respond!")
    print("Try asking questions, requesting summaries, or just chatting.\n")


def print_help():
    """Print help information"""
    print("\n" + "-"*60)
    print("HELP MENU - PERSISTENT MEMORY AI")
    print("-"*60)
    print("""
Available Features:

1. Question Answering
   - Ask any question starting with: what, how, why, when, where, who, which
   - Example: "What is machine learning?"

2. Conversational Chat
   - Just type a regular message
   - I'll respond naturally
   - Example: "Tell me a joke"

3. Sentiment Analysis
   - Text is analyzed for sentiment (positive/negative/neutral)
   - Shown in response metadata

4. Text Summarization
   - Use words like: summarize, summary, brief, condense
   - Example: "Summarize this long article..."

5. Persistent Memory (NEW!)
   - All interactions are saved automatically
   - Memories are organized by type and tagged
   - Auto-saves every 5 interactions
   - Survives between sessions

6. Memory Commands (NEW!)
   - /recall "query"     - Find related memories
   - /search "tag"       - Search by tag (e.g., learning, preference)
   - /profile            - See learned user profile
   - /save               - Force save to disk
   - /export "path"      - Export all data to ZIP

Commands:
  /help                - Show this menu
  /stats               - Show all statistics
  /memory              - Display session conversation history
  /recall [query]      - Recall memories related to query
  /search [tag]        - Search memories by tag
  /profile             - Show user profile from memories
  /clear               - Clear session memory (keeps persistent data)
  /save                - Force save all data now
  /export [path]       - Export all data to zip file
  /exit                - Exit the program

Memory Tags:
  - interaction        : Regular conversations
  - learning          : Things I learned about you
  - preference        : Your preferences
  - habit             : Your habits
  - interest          : Your interests
    """)
    print("-"*60)


def show_stats(ai: AIAssistant):
    """Display comprehensive AI statistics"""
    stats = ai.get_stats()
    print("\n" + "-"*60)
    print("AI ASSISTANT STATISTICS")
    print("-"*60)
    
    print(f"\nSession Information:")
    print(f"  Session ID: {stats['session']['session_id']}")
    print(f"  Current Session Interactions: {stats['session']['interactions_this_session']}")
    print(f"  Session Messages: {stats['session']['memory_size']}")
    
    print(f"\nKnowledge Base:")
    print(f"  Total Entries: {stats['knowledge_base']['total_entries']}")
    print(f"  Total Categories: {stats['knowledge_base']['categories']}")
    print(f"  Total Accesses: {stats['knowledge_base']['total_accesses']}")
    print(f"  Avg Accesses/Entry: {stats['knowledge_base']['avg_accesses_per_entry']:.2f}")
    
    print(f"\nPersistent Memory:")
    mem_stats = stats['persistent_memory']
    print(f"  Total Memories: {mem_stats['total_memories']}")
    print(f"  Session Memories: {mem_stats['session_memories']}")
    print(f"  Memory Types: {mem_stats['memory_types']}")
    print(f"  Avg Importance: {mem_stats['avg_importance']:.2f}")
    print(f"  Total Memory Accesses: {mem_stats['total_accesses']}")
    print(f"  Avg Age (days): {mem_stats['avg_age_days']:.1f}")
    
    storage = mem_stats.get('storage', {})
    print(f"\nStorage:")
    print(f"  Total Size: {storage.get('total_size_mb', 0):.2f} MB")
    print(f"  Memories Size: {storage.get('memories_size_mb', 0):.2f} MB")
    print(f"  Conversations Size: {storage.get('conversations_size_mb', 0):.2f} MB")
    print(f"  Total Conversations: {storage.get('total_conversations', 0)}")
    
    print("-"*60)


def show_memory(ai: AIAssistant):
    """Display session conversation memory"""
    history = ai.memory.get_history()
    summary = ai.memory.get_summary()
    
    print("\n" + "-"*60)
    print("SESSION CONVERSATION HISTORY")
    print("-"*60)
    
    if not history:
        print("No conversation history yet.")
    else:
        for i, msg in enumerate(history[-10:], 1):
            sender = "You" if msg["sender"] == "user" else "AI"
            content = msg['content'][:100] + "..." if len(msg['content']) > 100 else msg['content']
            print(f"\n[{i}] {sender}:")
            print(f"    {content}")
    
    print(f"\nSummary:")
    print(f"  Total Messages: {summary['total_messages']}")
    print(f"  User Messages: {summary['user_messages']}")
    print(f"  AI Messages: {summary['assistant_messages']}")
    print("-"*60)


def show_recalled_memories(ai: AIAssistant, query: str):
    """Display recalled memories"""
    memories = ai.recall_memory(query, top_k=5)
    
    print("\n" + "-"*60)
    print(f"RECALLED MEMORIES FOR: '{query}'")
    print("-"*60)
    
    if not memories:
        print("No related memories found.")
    else:
        for i, mem in enumerate(memories, 1):
            print(f"\n[{i}] {mem['type'].upper()}")
            print(f"    Content: {mem['content'][:150]}...")
            print(f"    Similarity: {mem['similarity']:.2f}")
            print(f"    Importance: {mem['importance']:.2f}")
            print(f"    Age: {mem['age_days']} days")
            print(f"    Accesses: {mem['access_count']}")
    
    print("-"*60)


def search_memory_by_tag(ai: AIAssistant, tag: str):
    """Search memories by tag"""
    memories = ai.search_memories_by_tag(tag, top_k=10)
    
    print("\n" + "-"*60)
    print(f"MEMORIES WITH TAG: '{tag}'")
    print("-"*60)
    
    if not memories:
        print(f"No memories found with tag '{tag}'.")
    else:
        for i, mem in enumerate(memories, 1):
            print(f"\n[{i}] {mem['type'].upper()}")
            print(f"    Content: {mem['content'][:150]}...")
            print(f"    Tags: {', '.join(mem['tags'])}")
            print(f"    Created: {mem['created_at']}")
    
    print("-"*60)


def show_user_profile(ai: AIAssistant):
    """Display user profile built from memories"""
    profile = ai.get_user_profile()
    
    print("\n" + "-"*60)
    print("YOUR PROFILE (Built from Memories)")
    print("-"*60)
    
    print(f"\nPreferences:")
    if profile['preferences']:
        for key, value in profile['preferences'].items():
            print(f"  {key}: {value}")
    else:
        print("  (No preferences learned yet)")
    
    print(f"\nHabits:")
    if profile['habits']:
        for key, value in profile['habits'].items():
            print(f"  {key}: {value}")
    else:
        print("  (No habits learned yet)")
    
    print(f"\nInterests:")
    if profile['interests']:
        for interest in profile['interests']:
            print(f"  - {interest}")
    else:
        print("  (No interests identified yet)")
    
    print(f"\nLearned Information:")
    if profile['learned_information']:
        for info in profile['learned_information']:
            print(f"  - {info}")
    else:
        print("  (No information learned yet)")
    
    print("-"*60)


def main():
    """Main function"""
    # Initialize AI Assistant with persistent memory
    ai = AIAssistant()
    
    # Print welcome message
    print_welcome()
    
    # Main conversation loop
    try:
        while True:
            # Get user input
            user_input = input("\nYou: ").strip()
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input.startswith("/"):
                parts = user_input[1:].split(maxsplit=1)
                command = parts[0].lower()
                arg = parts[1] if len(parts) > 1 else None
                
                if command == "help":
                    print_help()
                elif command == "stats":
                    show_stats(ai)
                elif command == "memory":
                    show_memory(ai)
                elif command == "recall":
                    if arg:
                        show_recalled_memories(ai, arg)
                    else:
                        print("\nUsage: /recall <query>")
                elif command == "search":
                    if arg:
                        search_memory_by_tag(ai, arg)
                    else:
                        print("\nUsage: /search <tag>")
                elif command == "profile":
                    show_user_profile(ai)
                elif command == "clear":
                    ai.reset_memory()
                    print("\n✓ Session memory cleared. (Persistent memory preserved)")
                elif command == "save":
                    if ai.save_all_data():
                        print("\n✓ All data saved to persistent storage.")
                    else:
                        print("\n❌ Error saving data.")
                elif command == "export":
                    if arg:
                        if ai.export_all_data(arg):
                            print(f"\n✓ Data exported to {arg}.zip")
                        else:
                            print("\n❌ Error exporting data.")
                    else:
                        print("\nUsage: /export <path>")
                elif command == "exit":
                    # Auto-save before exit
                    print("\n💾 Saving all data...")
                    ai.save_all_data()
                    print("👋 Thank you for chatting! Goodbye!")
                    break
                else:
                    print(f"\n❌ Unknown command: /{command}")
                    print("Type /help for available commands.")
            else:
                # Process user input
                print("\n🤔 Thinking...")
                result = ai.process(user_input)
                
                # Display response
                print(f"\nAI: {result['response']}")
                
                # Show metadata if verbose
                if VERBOSE:
                    print(f"\n[Task: {result['task']}, Sentiment: {result['metadata'].get('sentiment', 'neutral')}, Session: {result['session_id']}]")
    
    except KeyboardInterrupt:
        print("\n\n💾 Saving data...")
        ai.save_all_data()
        print("👋 Goodbye! (interrupted)")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        if DEBUG:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
