"""
AI Detective Telegram Bot Package

This package contains all modules for the advanced AI detective Telegram bot
with humanization features and continuous Heroku deployment.
"""

# Package version
__version__ = "1.0.0"

# Package-level imports for easier access
from .ai_detective import AIDetective
from .humanizer import Humanizer
from .memory import ConversationMemory
from .language import LanguageProcessor
from .voice import VoiceProcessor
from .utilities import format_analysis, split_long_message

# Initialize package-level components
def init_package():
    """
    Initialize package components that need setup
    """
    # You can add any package initialization code here if needed
    pass

# Run initialization when package is imported
init_package()

# Package metadata
__all__ = [
    'AIDetective',
    'Humanizer',
    'ConversationMemory',
    'LanguageProcessor',
    'VoiceProcessor',
    'format_analysis',
    'split_long_message',
    '__version__'
]
