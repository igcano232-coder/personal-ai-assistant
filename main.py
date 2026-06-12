#!/usr/bin/env python3
"""
Main Entry Point: Personal AI Assistant CLI
"""
import sys
from core.inference import AIAssistant
from config import DEBUG, VERBOSE


def print_welcome():
    """Print welcome message"""
    print("\n" + "="*60)
    print("🤖 Personal AI Assistant v1.0")
    print("Built from scratch, no external APIs required")
    print("="*60)
    print("\nCommands:")
    print("  /help       - Show help menu")
    print("  /stats      - Show AI statistics")
    print("  /memory     - Show conversation memory")
    print("  /clear      - Clear conversation memory")
    print("  /exit       - Exit the assistant")
    print("\nOtherwise, just type your message and I'll respond!")
    print("Try asking questions, requesting summaries, or just chatting.\n")


def print_help():
    """Print help information"""
    print("\n" + "-"*60)
    print("HELP MENU")
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

5. Conversation Memory
   - I remember recent conversation context
   - Use /memory to see conversation history
   - Use /clear to reset memory

Commands:
  /help       - Show this menu
  /stats      - Show knowledge base and memory statistics
  /memory     - Display conversation history
  /clear      - Clear all conversation memory
  /exit       - Exit the program
    """)
    print("-"*60)


def show_stats(ai: AIAssistant):
    """Display AI statistics"""
    stats = ai.get_stats()
    print("\n" + "-"*60)
    print("AI ASSISTANT STATISTICS")
    print("-"*60)
    print(f"\nKnowledge Base:")
    print(f"  Total Entries: {stats['knowledge_base']['total_entries']}")
    print(f"  Total Categories: {stats['knowledge_base']['categories']}")
    print(f"  Total Accesses: {stats['knowledge_base']['total_accesses']}")
    print(f"  Avg Accesses/Entry: {stats['knowledge_base']['avg_accesses_per_entry']:.2f}")
    
    print(f"\nConversation Memory:")
    print(f"  Messages: {stats['memory_size']}")
    print(f"  Turns: {stats['total_interactions']}")
    print("-"*60)


def show_memory(ai: AIAssistant):
    """Display conversation memory"""
    history = ai.memory.get_history()
    summary = ai.memory.get_summary()
    
    print("\n" + "-"*60)
    print("CONVERSATION HISTORY")
    print("-"*60)
    
    if not history:
        print("No conversation history yet.")
    else:
        for i, msg in enumerate(history[-10:], 1):  # Show last 10 messages
            sender = "You" if msg["sender"] == "user" else "AI"
            print(f"\n[{i}] {sender}:")
            print(f"    {msg['content'][:100]}..." if len(msg['content']) > 100 else f"    {msg['content']}")
    
    print(f"\nSummary:")
    print(f"  Total Messages: {summary['total_messages']}")
    print(f"  User Messages: {summary['user_messages']}")
    print(f"  AI Messages: {summary['assistant_messages']}")
    print("-"*60)


def main():
    """Main function"""
    # Initialize AI Assistant
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
                command = user_input[1:].lower()
                
                if command == "help":
                    print_help()
                elif command == "stats":
                    show_stats(ai)
                elif command == "memory":
                    show_memory(ai)
                elif command == "clear":
                    ai.reset_memory()
                    print("\n✓ Conversation memory cleared.")
                elif command == "exit":
                    print("\n👋 Thank you for chatting! Goodbye!")
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
                    print(f"\n[Task: {result['task']}, Sentiment: {result['metadata'].get('sentiment', 'neutral')}]")
    
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye! (interrupted)")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        if DEBUG:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
