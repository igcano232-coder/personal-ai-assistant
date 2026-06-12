# Personal AI Assistant 🤖

A lightweight, offline personal AI assistant built from scratch. No external APIs required. Designed to be simple now, powerful later.

## Features

- **Multi-task AI**: Q&A, summarization, sentiment analysis, text classification
- **100% Offline**: No API dependencies - runs locally
- **Modular Architecture**: Easy to upgrade and extend
- **Simple Foundation**: Core NLP without heavy dependencies
- **Conversation Memory**: Context-aware responses

## Project Structure

```
personal-ai-assistant/
├── core/                    # Core AI engine
│   ├── __init__.py
│   ├── tokenizer.py         # Text tokenization & preprocessing
│   ├── knowledge_base.py    # Knowledge storage & retrieval
│   └── inference.py         # Inference engine
├── tasks/                   # Multi-task modules
│   ├── __init__.py
│   ├── qa.py               # Question answering
│   ├── summarization.py    # Text summarization
│   ├── sentiment.py        # Sentiment analysis
│   └── chat.py             # Conversational AI
├── utils/                  # Utilities
│   ├── __init__.py
│   ├── preprocessing.py    # Text preprocessing
│   └── memory.py           # Conversation memory
├── models/                 # Pre-trained models (future)
├── main.py                 # Main entry point
├── requirements.txt        # Dependencies
└── config.py              # Configuration
```

## Quick Start

```bash
# Clone the repository
git clone https://github.com/igcano232-coder/personal-ai-assistant.git
cd personal-ai-assistant

# Install dependencies
pip install -r requirements.txt

# Run the assistant
python main.py
```

## Roadmap

### Phase 1 (Current) - Foundation
- [x] Basic tokenization
- [x] Simple rule-based Q&A
- [x] Sentiment analysis
- [x] Text summarization
- [x] Conversation memory

### Phase 2 - Neural Networks
- [ ] Word embeddings (Word2Vec/GloVe)
- [ ] Basic neural networks (PyTorch)
- [ ] Transformer attention mechanisms

### Phase 3 - Advanced
- [ ] Fine-tuned language models
- [ ] Multi-modal capabilities
- [ ] Advanced reasoning

## Usage Examples

```python
from core.inference import AIAssistant

ai = AIAssistant()

# Ask a question
response = ai.ask("What is machine learning?")

# Get sentiment
sentiment = ai.analyze_sentiment("I love this!")

# Summarize text
summary = ai.summarize("Long article text here...")

# Chat with memory
chat = ai.chat("Tell me a joke")
```

## Requirements

- Python 3.8+
- NLTK (Natural Language Toolkit)
- NumPy
- Scikit-learn (for basic ML)

No heavy dependencies like TensorFlow (for now - add later when needed).

## Architecture Philosophy

**Keep It Simple, Make It Scalable**

1. **Separation of Concerns**: Each module has one responsibility
2. **Pluggable Tasks**: Add new tasks without modifying core
3. **Upgrade Path**: Easy to replace simple components with ML/DL equivalents
4. **Local Only**: All processing happens offline

## Contributing

This is your personal project. Feel free to customize and extend!

## License

MIT
