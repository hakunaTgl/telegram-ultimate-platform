"""
Core modules for Telegram Ultimate Platform
"""

__version__ = "1.0.0"
__author__ = "hakunaTgl"

from core.context import build_context, MessageContext
from core.db import init_db
from core.intent import handle_intent
from core.privacy import require_opt_in, process_consent

__all__ = [
    'build_context',
    'MessageContext',
    'init_db',
    'handle_intent',
    'require_opt_in',
    'process_consent'
]
