import os
import random
from typing import List, Dict
from transformers import pipeline
import openai
import nltk
from nltk.tokenize import sent_tokenize

nltk.download('punkt')

class Humanizer:
    def __init__(self):
        self.paraphraser = pipeline(
            "text2text-generation",
            model="t5-base",
            device=-1
        )
        openai.api_key = os.getenv('OPENAI_API_KEY')
        self.filler_words = [
            'like', 'you know', 'I mean', 'well', 'actually',
            'basically', 'sort of', 'kind of', 'right', 'okay'
        ]
        self.discourse_markers = [
            'So', 'Anyway', 'Now', 'Then', 'Well',
            'Look', 'See', 'I think', 'I believe'
        ]

    def humanize(self, text: str, style: str = 'casual') -> str:
        """
        Transform text to sound more natural
        Styles: 'casual', 'professional', 'friendly'
        """
        # First pass - paraphrasing
        paraphrased = self._paraphrase(text)
        
        # Second pass - style adaptation
        styled = self._adapt_style(paraphrased, style)
        
        # Third pass - add natural features
        humanized = self._add_natural_features(styled, style)
        
        return humanized

    def _paraphrase(self, text: str) -> str:
        """Initial paraphrasing to break rigid structures"""
        result = self.paraphraser(
            f"paraphrase: {text}",
            max_length=len(text) + 100,
            do_sample=True,
            temperature=0.7,
            num_beams=3
        )
        return result[0]['generated_text']

    def _adapt_style(self, text: str, style: str) -> str:
        """Adapt text to specific communication style"""
        if style == 'professional':
            return self._make_professional(text)
        elif style == 'friendly':
            return self._make_friendly(text)
        else:  # casual
            return self._make_casual(text)

    def _make_casual(self, text: str) -> str:
        """Make text sound casual and conversational"""
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "system",
                "content": (
                    "Rewrite this text to sound like casual spoken conversation. "
                    "Use contractions, informal language, and conversational tone. "
                    "Keep the meaning identical but make it sound natural."
                )
            }, {
                "role": "user",
                "content": text
            }],
            temperature=0.8,
            max_tokens=1000
        )
        return response.choices[0].message.content

    def _make_professional(self, text: str) -> str:
        """Make text sound professional but not robotic"""
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "system",
                "content": (
                    "Rewrite this text to sound professional yet natural. "
                    "Avoid jargon but maintain formal tone. Use complete sentences "
                    "but don't sound robotic. Keep the meaning identical."
                )
            }, {
                "role": "user",
                "content": text
            }],
            temperature=0.6,
            max_tokens=1000
        )
        return response.choices[0].message.content

    def _make_friendly(self, text: str) -> str:
        """Make text sound warm and friendly"""
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "system",
                "content": (
                    "Rewrite this text to sound warm and friendly. "
                    "Use positive language and inclusive phrasing. "
                    "Imagine you're talking to a colleague you like. "
                    "Keep the meaning identical."
                )
            }, {
                "role": "user",
                "content": text
            }],
            temperature=0.7,
            max_tokens=1000
        )
        return response.choices[0].message.content

    def _add_natural_features(self, text: str, style: str) -> str:
        """Add natural speech characteristics"""
        sentences = sent_tokenize(text)
        
        # Add discourse markers
        if random.random() < 0.4 and len(sentences) > 1:
            sentences[0] = f"{random.choice(self.discourse_markers)}, {sentences[0].lower()}"
        
        # Add fillers for casual style
        if style == 'casual' and random.random() < 0.3:
            pos = random.randint(1, len(sentences)-1)
            sentences.insert(pos, random.choice(self.filler_words).capitalize())
        
        # Random sentence restructuring
        if random.random() < 0.2:
            sentences[-1] = sentences[-1].replace('.', ', you know?')
        
        return ' '.join(sentences)
