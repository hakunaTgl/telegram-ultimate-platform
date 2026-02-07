from core.db import save_user_profile, save_chat_profile

async def handle_intent(ctx):
    """Analyze message context and metadata to determine intent and update profiles."""
    u = ctx.user_profile.copy()
    c = ctx.chat_profile.copy()
    
    # Simple preference learning: count messages per chat, track last topics
    c["message_count"] = c.get("message_count", 0) + 1
    c.setdefault("keywords", [])
    
    # Infer space roles from metadata/content
    if "#task" in ctx.text.lower():
        c["role"] = "tasks"
    
    if any(domain in " ".join(ctx.links).lower() for domain in ["zoom.us", "meet.google.com"]):
        c["role"] = "events"
    
    # User preference: learn if they often request summaries
    if any(kw in ctx.text.lower() for kw in ["summary", "tl;dr", "summarize"]):
        u["pref_summaries"] = True
    
    # Persist the updated knowledge
    await save_user_profile(ctx.user_id, u)
    await save_chat_profile(ctx.chat_id, c)
    
    # Dispatch to specialized handlers based on inferred roles
    role = c.get("role")
    if role == "tasks":
        return await handle_task_space(ctx, u, c)
    elif role == "events":
        return await handle_event_space(ctx, u, c)
    else:
        return await handle_default(ctx, u, c)

async def handle_task_space(ctx, u, c):
    """Handle interactions in a task-oriented context."""
    text = ctx.text.lower()
    if text.startswith("todo") or "add task" in text:
        return "Captured a new task. I've logged it in your persistent task list."
    if "remind me" in text:
        return "I'll set up a reminder based on this context. When should I alert you?"
    return "This space is optimized for tasks. Should I log this message or set a reminder?"

async def handle_event_space(ctx, u, c):
    """Handle interactions in an event/promo oriented context."""
    if ctx.links:
        return f"Detected an event link: {ctx.links[0]}
Would you like me to extract the schedule and add it to your calendar?"
    return "This appears to be an events/promo channel. I can provide a daily summary of all shared links."

async def handle_default(ctx, u, c):
    """Default fallback as the bot learns the context."""
    return "I'm still learning the purpose of this space. Is this for tasks, events, or general chat? I'll adapt accordingly."
