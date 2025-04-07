from typing import Dict, Any

def format_analysis(analysis: Dict[str, Any]) -> str:
    """Format analysis results for Telegram message"""
    entities = "\n".join(
        f"- {e['word']} ({e['entity']}, confidence: {e['score']:.2f})" 
        for e in analysis['entities'][:5]
    )
    
    return (
        f"🔍 Deep Analysis Report\n\n"
        f"📊 Sentiment: {analysis['sentiment']['label']} (confidence: {analysis['sentiment']['score']:.2f})\n"
        f"🎭 Deception Score: {analysis['deception_score']:.2f}/1.00\n\n"
        f"🏷️ Top Entities:\n{entities}\n\n"
        f"🧠 AI Insights:\n{analysis['insights']}\n\n"
        f"✍️ Writing Patterns:\n"
        f"- Avg. sentence length: {analysis['writing_patterns']['avg_sentence_length']:.1f} chars\n"
        f"- Word diversity: {analysis['writing_patterns']['word_diversity']:.2f}"
    )

def split_long_message(text: str, max_length: int = 4000) -> List[str]:
    """Split long text into chunks for Telegram messages"""
    if len(text) <= max_length:
        return [text]
    
    parts = []
    while text:
        part = text[:max_length]
        last_newline = part.rfind('\n')
        if last_newline > 0:
            part = part[:last_newline]
        parts.append(part)
        text = text[len(part):].lstrip()
    
    return parts
