"""
Context Extraction and Metadata Learning Module

This module normalizes Telegram updates into structured records
and extracts metadata signals for adaptive learning.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any, Optional
from telegram import Update
from core.db import get_user_profile, get_chat_profile, log_interaction

@dataclass
class MessageContext:
    """
    Normalized representation of a message with enriched metadata
    """
    chat_id: int
    user_id: int
    text: str
    timestamp: datetime
    is_group: bool
    chat_type: str
    links: List[str] = field(default_factory=list)
    hashtags: List[str] = field(default_factory=list)
    media_type: Optional[str] = None
    user_profile: Dict[str, Any] = field(default_factory=dict)
    chat_profile: Dict[str, Any] = field(default_factory=dict)
    
    # Derived signals
    is_event_related: bool = False
    is_task_related: bool = False
    language: Optional[str] = None

async def build_context(update: Update) -> MessageContext:
    """
    Normalize a Telegram update into a MessageContext record
    """
    msg = update.message
    if not msg:
        return None
        
    chat = msg.chat
    user = msg.from_user
    text = msg.text or ""
    
    # Extract entities (links, hashtags)
    links = []
    hashtags = []
    if msg.entities:
        for entity in msg.entities:
            if entity.type == 'url':
                links.append(text[entity.offset:entity.offset + entity.length])
            elif entity.type == 'text_link':
                links.append(entity.url)
            elif entity.type == 'hashtag':
                hashtags.append(text[entity.offset:entity.offset + entity.length])
    
    # Determine media type
    media_type = None
    if msg.photo: media_type = 'photo'
    elif msg.video: media_type = 'video'
    elif msg.document: media_type = 'document'
    elif msg.voice: media_type = 'voice'
    
    # Load memory/profiles
    user_profile = await get_user_profile(user.id)
    chat_profile = await get_chat_profile(chat.id)
    
    # Initial metadata signals
    is_event_related = any("zoom.us" in link or "meet.google.com" in link for link in links)
    is_task_related = "#task" in hashtags or text.lower().startswith(("todo:", "remind me"))
    
    ctx = MessageContext(
        chat
      _id=chat.id,
        user_id=user.id,
        text=text,
        timestamp=msg.date,
        is_group=chat.type in ("group", "supergroup"),
        chat_type=chat.type,
        links=links,
        hashtags=hashtags,
        media_type=media_type,
        user_profile=user_profile,
        chat_profile=chat_profile,
        is_event_related=is_event_related,
        is_task_related=is_task_related,
        language=user.language_code
    )
    
    # Log interaction for future learning
    await log_interaction(ctx)
    
    return ctx
