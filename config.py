# Configuration file for Personal AI Assistant

# Model settings
MODEL_CONFIG = {
    "max_response_length": 500,
    "memory_size": 50,  # Number of past messages to remember
    "confidence_threshold": 0.5,
}

# Tokenizer settings
TOKENIZER_CONFIG = {
    "lowercase": True,
    "remove_punctuation": True,
    "remove_stopwords": False,  # Can be enabled later for optimization
}

# Knowledge base settings
KB_CONFIG = {
    "max_knowledge_entries": 1000,
    "similarity_threshold": 0.6,
}

# Task settings
TASKS_CONFIG = {
    "qa": {"enabled": True, "priority": 1},
    "chat": {"enabled": True, "priority": 2},
    "sentiment": {"enabled": True, "priority": 3},
    "summarization": {"enabled": True, "priority": 4},
}

# Debug settings
DEBUG = True
VERBOSE = True
