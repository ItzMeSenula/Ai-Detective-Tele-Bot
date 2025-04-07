from googletrans import Translator
from typing import Tuple, Optional

class LanguageProcessor:
    def __init__(self):
        self.translator = Translator()
        self.language_names = {
            'en': 'English',
            'si': 'Sinhala',
            'ta': 'Tamil',
            'fr': 'French',
            'es': 'Spanish',
            'de': 'German',
            'it': 'Italian',
            'ru': 'Russian',
            'zh-cn': 'Chinese (Simplified)',
            'ja': 'Japanese',
            'ko': 'Korean'
        }

    def detect(self, text: str) -> str:
        """Detect language and return its name"""
        try:
            detected = self.translator.detect(text)
            return self.language_names.get(detected.lang, detected.lang)
        except:
            return "Unknown"

    def translate(self, text: str, target: str = 'en') -> Tuple[Optional[str], Optional[str]]:
        """Translate text to target language"""
        try:
            result = self.translator.translate(text, dest=target)
            return result.text, self.language_names.get(result.src, result.src)
        except Exception as e:
            print(f"Translation error: {e}")
            return None, None
