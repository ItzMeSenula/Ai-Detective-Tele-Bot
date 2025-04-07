import os
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)
from bot.ai_detective import AIDetective
from bot.humanizer import Humanizer
from bot.memory import ConversationMemory
from bot.language import LanguageProcessor
from bot.voice import VoiceProcessor
from bot.utilities import format_analysis

# Initialize modules
detective = AIDetective()
humanizer = Humanizer()
memory = ConversationMemory()
language = LanguageProcessor()
voice = VoiceProcessor()

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_msg = (
        f"👋 Hi {user.first_name}! I'm your AI Detective Bot.\n\n"
        "🔍 Send me text to analyze or use these commands:\n"
        "/analyze - Deep AI analysis\n"
        "/humanize - Make text natural\n"
        "/language - Detect language\n"
        "/help - Show all commands"
    )
    await update.message.reply_text(welcome_msg)

async def analyze_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = ' '.join(context.args) or memory.recall(update.effective_user.id, 'last_message')
    if not text:
        await update.message.reply_text("Please provide text to analyze or send a message first.")
        return
    
    try:
        analysis = detective.analyze(text)
        memory.store(update.effective_user.id, 'last_analysis', analysis)
        await update.message.reply_text(format_analysis(analysis))
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        await update.message.reply_text("⚠️ Analysis failed. Please try again.")

async def humanize_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = ' '.join(context.args) or memory.recall(update.effective_user.id, 'last_message')
    if not text:
        await update.message.reply_text("Please provide text to humanize or send a message first.")
        return
    
    try:
        humanized = humanizer.humanize(text)
        await update.message.reply_text(f"💬 Humanized version:\n\n{humanized}")
    except Exception as e:
        logger.error(f"Humanization failed: {e}")
        await update.message.reply_text("⚠️ Humanization failed. Please try again.")

async def detect_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = ' '.join(context.args) or memory.recall(update.effective_user.id, 'last_message')
    if not text:
        await update.message.reply_text("Please provide text or send a message first.")
        return
    
    try:
        lang = language.detect(text)
        await update.message.reply_text(f"🌐 Detected language: {lang}")
    except Exception as e:
        logger.error(f"Language detection failed: {e}")
        await update.message.reply_text("⚠️ Language detection failed.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    memory.store(user_id, 'last_message', text)
    
    quick_analysis = detective.quick_analyze(text)
    response = (
        f"🔍 Quick Analysis:\n\n"
        f"📊 Sentiment: {quick_analysis['sentiment']}\n"
        f"🏷️ Key Entities: {', '.join(quick_analysis['entities'][:5])}\n\n"
        f"Use /analyze for deeper inspection or /humanize to make this more natural."
    )
    await update.message.reply_text(response)

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        voice_file = await update.message.voice.get_file()
        voice_path = f"voice_{update.update_id}.ogg"
        await voice_file.download_to_drive(voice_path)
        
        text = voice.to_text(voice_path)
        os.remove(voice_path)
        
        memory.store(update.effective_user.id, 'last_message', text)
        await update.message.reply_text(f"🎤 Transcribed text:\n\n{text}")
    except Exception as e:
        logger.error(f"Voice processing failed: {e}")
        await update.message.reply_text("⚠️ Voice message processing failed.")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Update {update} caused error {context.error}")
    if update and hasattr(update, 'effective_chat'):
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="⚠️ Sorry, I encountered an error processing your request."
        )

def main():
    application = ApplicationBuilder() \
        .token(os.getenv('TELEGRAM_TOKEN')) \
        .post_init(lambda _: logger.info("Bot initialized")) \
        .build()
    
    # Command handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', start))
    application.add_handler(CommandHandler('analyze', analyze_text))
    application.add_handler(CommandHandler('humanize', humanize_text))
    application.add_handler(CommandHandler('language', detect_language))
    
    # Message handlers
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.VOICE, handle_voice))
    
    # Error handler
    application.add_error_handler(error_handler)
    
    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
