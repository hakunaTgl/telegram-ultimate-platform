-- User Profiles table for long-term memory and preferences
CREATE TABLE IF NOT EXISTS user_profiles (
    user_id BIGINT PRIMARY KEY,
    data JSONB DEFAULT '{}'
);

-- Chat Profiles table for space roles and context learning
CREATE TABLE IF NOT EXISTS chat_profiles (
    chat_id BIGINT PRIMARY KEY,
    data JSONB DEFAULT '{}'
);

-- Interaction Log for metadata learning and adaptive history
CREATE TABLE IF NOT EXISTS interaction_log (
    id SERIAL PRIMARY KEY,
    chat_id BIGINT,
    user_id BIGINT,
    ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    text TEXT,
    is_group BOOLEAN,
    links TEXT[]
);
