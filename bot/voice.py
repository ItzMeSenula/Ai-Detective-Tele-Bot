import os
import speech_recognition as sr
from pydub import AudioSegment
from typing import Optional

class VoiceProcessor:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        
    def to_text(self, audio_path: str) -> Optional[str]:
        """Convert voice message to text"""
        try:
            # Convert OGG to WAV
            sound = AudioSegment.from_ogg(audio_path)
            wav_path = audio_path.replace('.ogg', '.wav')
            sound.export(wav_path, format="wav")
            
            # Recognize speech
            with sr.AudioFile(wav_path) as source:
                audio = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio)
            
            os.remove(wav_path)
            return text
        except Exception as e:
            print(f"Voice processing failed: {e}")
            return None
