#!/usr/bin/env python3
"""
Telegram Ultimate Platform - Main Application
A complete, self-adaptive Telegram assistant.
"""
import os
import sys
import asyncio
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# Import core modules
from core.context import build_context
from core.intent import handle_intent
from core.privacy import require_opt_in, process_consent
from core.db import init_db, get_user_profile, update_user_metadata
from core.ai import AIEngine
from core.tasks import TaskManager

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configuration
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://localhost/telegram_assistant')

if not BOT_TOKEN:
    logger.error("TELEGRAM_BOT_TOKEN environment variable not set!")
    sys.exit(1)

# Initialize Core Components
ai_engine = AIEngine()
task_manager = TaskManager()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command."""
    user_id = update.effective_user.id
    await require_opt_in(update, context, user_id)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command."""
    help_text = "🤖 *Telegram Ultimate Assistant*
I'm a self-adaptive assistant that learns from you!

/start - Initialize
/help - Show this
/forget_me - Delete data
/export_me - Export data"
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def on_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Main processing pipeline."""
    text = (update.message.text or "").strip().lower()
    user_id = update.effective_user.id

    if text in ['yes', 'no']:
        await process_consent(update)
        return

    ctx = await build_context(update)
    intent_reply = await handle_intent(ctx)
    
    if not intent_reply:
        profile = await get_user_profile(user_id)
        reply = await ai_engine.generate_response(update.message.text, ctx, profile)
        new_metadata = await ai_engine.extract_metadata(update.message.text)
        if new_metadata:
            await update_user_metadata(user_id, new_metadata)
    else:
        reply = intent_reply

    if reply:
        await update.message.reply_text(reply)

async def forget_me_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from core.db import delete_user_data
    user_id = update.effective_user.id
    await delete_user_data(user_id)
    await update.message.reply_text("✅ All your data has been deleted.")

async def export_me_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from core.db import export_user_data
    import json
    user_id = update.effective_user.id
    user_data = await export_user_data(user_id)
    data_json = json.dumps(user_data, indent=2)
    await update.message.reply_document(
        document=data_json.encode('utf-8'),
        filename=f'data_{user_id}.json',
        caption="📦 Your data export."
    )

def main():
    """Main entry point."""
    logger.info("Starting Platform...")
    task_manager.start()
    asyncio.get_event_loop().run_until_complete(init_db(DATABASE_URL))
    
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("forget_me", forget_me_command))
    app.add_handler(CommandHandler("export_me", export_me_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_message))
    
    app.run_polling()

if __name__ == "__main__":
    main()
