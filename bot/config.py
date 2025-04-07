import os
from dotenv import load_dotenv
from typing import Dict, Any, Optional
import logging

# Load environment variables from .env file
load_dotenv()

class Config:
    """
    Central configuration class for the AI Detective Bot.
    Handles all environment variables and default settings.
    """
    
    # Telegram Bot Configuration
    TELEGRAM_TOKEN: str = os.getenv('TELEGRAM_TOKEN', '')
    ADMIN_IDS: list = [int(id) for id in os.getenv('ADMIN_IDS', '').split(',') if id]
    BOT_NAME: str = os.getenv('BOT_NAME', 'AI Detective Bot')
    
    # AI Services Configuration
    OPENAI_API_KEY: str = os.getenv('OPENAI_API_KEY', '')
    OPENAI_MODEL: str = os.getenv('OPENAI_MODEL', 'gpt-4')
    HUGGINGFACE_TOKEN: str = os.getenv('HUGGINGFACE_TOKEN', '')
    
    # Heroku/Server Configuration
    HEROKU_APP_NAME: str = os.getenv('HEROKU_APP_NAME', '')
    PORT: int = int(os.getenv('PORT', '8443'))
    WEBHOOK_URL: str = f"https://{HEROKU_APP_NAME}.herokuapp.com/" if HEROKU_APP_NAME else ''
    
    # Feature Toggles
    ENABLE_VOICE: bool = os.getenv('ENABLE_VOICE', 'true').lower() == 'true'
    ENABLE_ANALYSIS: bool = os.getenv('ENABLE_ANALYSIS', 'true').lower() == 'true'
    ENABLE_HUMANIZATION: bool = os.getenv('ENABLE_HUMANIZATION', 'true').lower() == 'true'
    
    # Rate Limiting
    REQUESTS_PER_MINUTE: int = int(os.getenv('REQUESTS_PER_MINUTE', '30'))
    MESSAGE_CHAR_LIMIT: int = int(os.getenv('MESSAGE_CHAR_LIMIT', '4000'))
    
    # Localization
    DEFAULT_LANGUAGE: str = os.getenv('DEFAULT_LANGUAGE', 'en')
    SUPPORTED_LANGUAGES: list = os.getenv('SUPPORTED_LANGUAGES', 'en,si,ta').split(',')
    
    # Paths
    DATA_DIR: str = os.getenv('DATA_DIR', 'data')
    LOG_FILE: str = os.path.join(DATA_DIR, 'bot.log')
    MEMORY_FILE: str = os.path.join(DATA_DIR, 'memory.json')
    
    @classmethod
    def validate(cls) -> bool:
        """Validate essential configurations"""
        errors = []
        
        if not cls.TELEGRAM_TOKEN:
            errors.append("TELEGRAM_TOKEN is required")
            
        if not cls.OPENAI_API_KEY:
            errors.append("OPENAI_API_KEY is required")
            
        if cls.ENABLE_VOICE and not cls.HUGGINGFACE_TOKEN:
            errors.append("HUGGINGFACE_TOKEN is required when voice is enabled")
            
        if errors:
            for error in errors:
                logging.error(f"Configuration Error: {error}")
            return False
        return True
    
    @classmethod
    def get_all_settings(cls) -> Dict[str, Any]:
        """Return all current settings (excluding sensitive data)"""
        return {
            'bot_name': cls.BOT_NAME,
            'heroku_app': cls.HEROKU_APP_NAME,
            'features': {
                'voice': cls.ENABLE_VOICE,
                'analysis': cls.ENABLE_ANALYSIS,
                'humanization': cls.ENABLE_HUMANIZATION
            },
            'limits': {
                'requests_per_minute': cls.REQUESTS_PER_MINUTE,
                'message_length': cls.MESSAGE_CHAR_LIMIT
            },
            'localization': {
                'default_language': cls.DEFAULT_LANGUAGE,
                'supported_languages': cls.SUPPORTED_LANGUAGES
            }
        }

# Initialize data directory
os.makedirs(Config.DATA_DIR, exist_ok=True)

# Validate configuration on import
if not Config.validate():
    raise RuntimeError("Invalid configuration. Please check your environment variables.")
