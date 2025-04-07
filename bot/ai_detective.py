import os
from typing import Dict, List, Any
from transformers import pipeline
import openai
import spacy
import numpy as np

class AIDetective:
    def __init__(self):
        self.sentiment_analyzer = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english"
        )
        self.ner_pipeline = pipeline(
            "ner",
            model="dbmdz/bert-large-cased-finetuned-conll03-english",
            aggregation_strategy="simple"
        )
        self.nlp = spacy.load("en_core_web_sm")
        openai.api_key = os.getenv('OPENAI_API_KEY')
        self.deception_model = self._load_deception_model()

    def analyze(self, text: str) -> Dict[str, Any]:
        """Comprehensive text analysis"""
        sentiment = self._analyze_sentiment(text)
        entities = self._extract_entities(text)
        deception = self._detect_deception(text)
        patterns = self._detect_patterns(text)
        insights = self._get_insights(text, sentiment, entities, deception)
        
        return {
            'sentiment': sentiment,
            'entities': entities,
            'deception_score': deception,
            'writing_patterns': patterns,
            'insights': insights,
            'raw_text': text
        }

    def quick_analyze(self, text: str) -> Dict[str, Any]:
        """Fast analysis for real-time responses"""
        sentiment = self._analyze_sentiment(text)
        entities = self._extract_key_entities(text)
        
        return {
            'sentiment': sentiment['label'],
            'entities': entities
        }

    def _analyze_sentiment(self, text: str) -> Dict[str, Any]:
        result = self.sentiment_analyzer(text[:512])[0]
        return {'label': result['label'], 'score': float(result['score'])}

    def _extract_entities(self, text: str) -> List[Dict[str, Any]]:
        results = self.ner_pipeline(text[:512])
        return [{
            'word': ent['word'],
            'entity': ent['entity_group'],
            'score': float(ent['score'])
        } for ent in results]

    def _extract_key_entities(self, text: str) -> List[str]:
        doc = self.nlp(text[:512])
        return [ent.text for ent in doc.ents if ent.label_ in ['PERSON', 'ORG', 'GPE']][:5]

    def _detect_deception(self, text: str) -> float:
        """Analyze text for deception patterns"""
        features = self._extract_deception_features(text)
        return float(self.deception_model.predict([features])[0])

    def _extract_deception_features(self, text: str) -> List[float]:
        """Extract linguistic features for deception detection"""
        doc = self.nlp(text)
        return [
            len(text),
            len(text.split()),
            sum(1 for _ in doc.sents),
            sum(1 for token in doc if token.is_punct),
            sum(1 for token in doc if token.lemma_ in ['i', 'me', 'my']),
            sum(1 for token in doc if token.lemma_ in ['we', 'us', 'our'])
        ]

    def _detect_patterns(self, text: str) -> Dict[str, Any]:
        """Detect writing style patterns"""
        doc = self.nlp(text)
        return {
            'avg_sentence_length': np.mean([len(sent) for sent in doc.sents]),
            'word_diversity': len(set(token.text for token in doc)) / len(doc),
            'pos_ratios': {
                'nouns': sum(1 for token in doc if token.pos_ == 'NOUN') / len(doc),
                'verbs': sum(1 for token in doc if token.pos_ == 'VERB') / len(doc),
                'adjectives': sum(1 for token in doc if token.pos_ == 'ADJ') / len(doc)
            }
        }

    def _get_insights(self, text: str, sentiment: Dict, entities: List, deception: float) -> str:
        """Generate human-readable insights"""
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{
                "role": "system",
                "content": (
                    "You're an AI detective analyzing text. Provide concise, insightful analysis "
                    "about the text's sentiment, entities, potential deception, and any unusual patterns. "
                    "Keep it professional but accessible."
                )
            }, {
                "role": "user",
                "content": (
                    f"Text: {text}\n\n"
                    f"Sentiment: {sentiment['label']} (confidence: {sentiment['score']:.2f})\n"
                    f"Key Entities: {', '.join(e['word'] for e in entities[:5])}\n"
                    f"Deception Score: {deception:.2f}\n\n"
                    "Provide your analysis:"
                )
            }],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content

    def _load_deception_model(self):
        """Load deception detection model (placeholder implementation)"""
        from sklearn.linear_model import LogisticRegression
        model = LogisticRegression()
        model.coef_ = np.array([[0.1, -0.2, 0.05, -0.1, 0.3, -0.15]])
        model.intercept_ = np.array([-0.5])
        return model
