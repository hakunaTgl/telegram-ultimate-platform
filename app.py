#!/usr/bin/env python3
"""
Telegram Ultimate Platform - Main Application

A complete, self-adaptive Telegram assistant with:
- Bot API integration
- Metadata learning and context awareness
- Adaptive intent engine
- Privacy-compliant data handling
- Multi-account support
- Task automation

Author: hakunaTgl
License: MIT
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
from core.db import init_db

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


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle /start command - initial user interaction
    """
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    
    logger.info(f"User {user_id} ({user_name}) started the bot")
    
    # Request opt-in for personalization
    await require_opt_in(update, context, user_id)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle /help command
    """
    help_text = """
🤖 *Telegram Ultimate Assistant*

I'm a self-adaptive assistant that learns from your interactions!

*Commands:*
/start - Initialize the bot
/help - Show this message
/settings - View and change your preferences
/forget_me - Delete all your data
/export_me - Export your data

*Features:*
✓ Adaptive learning from metadata
✓ Context-aware responses
✓ Task automation
✓ Privacy-compliant data handling
✓ Multi-space support (tasks, events, general)

*How it works:*
Just chat naturally! I'll learn your preferences over time:
- Use #task for task-related chats
- Share Zoom links in event channels
- Say "summary" or "tl;dr" if you like summaries

I adapt to each chat's purpose automatically!
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')


async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle /settings command
    """
    # TODO: Implement settings menu with inline keyboard
    await update.message.reply_text(
        "⚙️ Settings menu coming soon!\n\n"
        "For now, you can:\n"
        "- Type 'this is for tasks' to mark a chat\n"
        "- Type 'this is events' to mark event channels\n"
        "- Type 'stop doing X here' to override behaviors"
    )


async def forget_me_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle /forget_me command - GDPR compliance
    """
    from core.db import delete_user_data
    
    user_id = update.effective_user.id
    await delete_user_data(user_id)
    
    await update.message.reply_text(
        "✅ All your data has been deleted.\n\n"
        "I'll no longer store personalization data for you."
    )
    logger.info(f"User {user_id} requested data deletion")


async def export_me_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle /export_me command - GDPR compliance
    """
    from core.db import export_user_data
    import json
    
    user_id = update.effective_user.id
    user_data = await export_user_data(user_id)
    
    # Send as JSON file
    data_json = json.dumps(user_data, indent=2)
    await update.message.reply_document(
        document=data_json.encode('utf-8'),
        filename=f'telegram_data_{user_id}.json',
        caption="📦 Here's all your stored data!"
    )
    logger.info(f"User {user_id} exported their data")


async def on_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle all text messages - main processing pipeline
    """
    # Check for consent messages first
    text = (update.message.text or "").strip().lower()
    if text in ['yes', 'no']:
        await process_consent(update)
        return
    
    # Build context with metadata
    ctx = await build_context(update)
    
    # Process through intent engine
    reply = await handle_intent(ctx)
    
    # Send response if any
    if reply:
        await update.message.reply_text(reply)


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle errors in the bot
    """
    logger.error(f"Exception while handling an update: {context.error}")
    
    if isinstance(update, Update) and update.effective_message:
        await update.effective_message.reply_text(
            "❌ Sorry, something went wrong! Please try again."
        )


def main():
    """
    Main entry point
    """
    logger.info("Starting Telegram Ultimate Platform...")
    
    # Initialize database
    asyncio.get_event_loop().run_until_complete(init_db(DATABASE_URL))
    logger.info("Database initialized")
    
    # Create application
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Register command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("settings", settings_command))
    app.add_handler(CommandHandler("forget_me", forget_me_command))
    app.add_handler(CommandHandler("export_me", export_me_command))
    
    # Register message handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_message))
    
    # Register error handler
    app.add_error_handler(error_handler)
    
    # Start the bot
    logger.info("Bot started! Press Ctrl+C to stop.")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
