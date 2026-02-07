import asyncpg
import json
import logging

# Database connection pool
POOL = None

async def init_db(dsn: str):
    """Initialize the database connection pool."""
    global POOL
    try:
        POOL = await asyncpg.create_pool(dsn)
        logging.info("Database connection pool initialized.")
    except Exception as e:
        logging.error(f"Failed to initialize database: {e}")
        raise

async def get_user_profile(user_id: int) -> dict:
    """Retrieve user profile from the database."""
    async with POOL.acquire() as conn:
        row = await conn.fetchrow("SELECT data FROM user_profiles WHERE user_id=$1", user_id)
        return json.loads(row["data"]) if row and row["data"] else {}

async def get_chat_profile(chat_id: int) -> dict:
    """Retrieve chat profile from the database."""
    async with POOL.acquire() as conn:
        row = await conn.fetchrow("SELECT data FROM chat_profiles WHERE chat_id=$1", chat_id)
        return json.loads(row["data"]) if row and row["data"] else {}

async def save_user_profile(user_id: int, data: dict):
    """Save or update user profile in the database."""
    async with POOL.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO user_profiles (user_id, data)
            VALUES ($1, $2)
            ON CONFLICT (user_id) DO UPDATE SET data = EXCLUDED.data
            """,
            user_id, json.dumps(data)
        )

async def save_chat_profile(chat_id: int, data: dict):
    """Save or update chat profile in the database."""
    async with POOL.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO chat_profiles (chat_id, data)
            VALUES ($1, $2)
            ON CONFLICT (chat_id) DO UPDATE SET data = EXCLUDED.data
            """,
            chat_id, json.dumps(data)
        )

async def log_interaction(ctx):
    """Log user interaction for adaptive learning."""
    async with POOL.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO interaction_log (chat_id, user_id, ts, text, is_group, links)
            VALUES ($1, $2, $3, $4, $5, $6)
            """,
            ctx.chat_id, ctx.user_id, ctx.timestamp, ctx.text, ctx.is_group, ctx.links
        )

async def close_db():
    """Close the database connection pool."""
    if POOL:
        await POOL.close()
        logging.info("Database connection pool closed.")

async def delete_user_data(user_id: int):
    """Delete all stored data for a user (GDPR compliance)."""
    async with POOL.acquire() as conn:
        await conn.execute("DELETE FROM user_profiles WHERE user_id=$1", user_id)
        await conn.execute("DELETE FROM interaction_log WHERE user_id=$1", user_id)

async def export_user_data(user_id: int) -> dict:
    """Export all stored data for a user (GDPR compliance)."""
    async with POOL.acquire() as conn:
        profile_row = await conn.fetchrow("SELECT data FROM user_profiles WHERE user_id=$1", user_id)
        interaction_rows = await conn.fetch("SELECT ts, text, is_group, links FROM interaction_log WHERE user_id=$1", user_id)
        
        return {
            "profile": json.loads(profile_row["data"]) if profile_row else {},
            "interactions": [
                {
                    "timestamp": r["ts"].isoformat() if r["ts"] else None,
                    "text": r["text"],
                    "is_group": r["is_group"],
                    "links": r["links"]
                } for r in interaction_rows
            ]
        }

async def create_tables():
    """Create necessary database tables if they do not exist."""
    async with POOL.acquire() as conn:
        await conn.execute(\"\"\"
            CREATE TABLE IF NOT EXISTS user_profiles (
                user_id BIGINT PRIMARY KEY,
                data JSONB DEFAULT '{}'
            );
            CREATE TABLE IF NOT EXISTS chat_profiles (
                chat_id BIGINT PRIMARY KEY,
                data JSONB DEFAULT '{}'
            );
            CREATE TABLE IF NOT EXISTS interaction_log (
                id SERIAL PRIMARY KEY,
                chat_id BIGINT,
                user_id BIGINT,
                ts TIMESTAMP WITH TIME ZONE,
                text TEXT,
                is_group BOOLEAN,
                links TEXT[]
            );
        \"\"\")
