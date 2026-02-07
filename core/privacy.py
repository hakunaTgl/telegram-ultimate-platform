from telegram import Update
from telegram.ext import ContextTypes
from core.db import get_user_profile, save_user_profile

CONSENT_KEY = "consent_personalization"

async def require_opt_in(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int):
    """Check if user has consented to data collection for personalization."""
    profile = await get_user_profile(user_id)
    if profile.get(CONSENT_KEY):
        return True
        
    # Provide a clear, lawful notice about data usage
    await update.message.reply_text(
        "I can adapt to your needs by learning from your interaction patterns and shared metadata. "
        "This data is stored securely and used only to improve your experience. "
        "Reply 'yes' to enable intelligent adaptation or 'no' to remain stateless."
    )
    return False

async def process_consent(update: Update):
    """Handle the user's response to the privacy/consent prompt."""
    user_id = update.effective_user.id
    text = (update.message.text or "").strip().lower()
    profile = await get_user_profile(user_id)
    
    if text == "yes":
        profile[CONSENT_KEY] = True
        await save_user_profile(user_id, profile)
        await update.message.reply_text("Intelligence adaptation enabled. I'll start learning from our interactions now.")
    elif text == "no":
        profile[CONSENT_KEY] = False
        await save_user_profile(user_id, profile)
        await update.message.reply_text("Stateless mode confirmed. I won't store interaction data for this account.")
