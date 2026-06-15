# 🤖 Telegram Ultimate Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Telegram Bot API](https://img.shields.io/badge/Telegram-Bot%20API-26A5E4?logo=telegram)](https://core.telegram.org/bots/api)
[![Status: Active](https://img.shields.io/badge/Status-Active-brightgreen.svg)](#)

> A complete, self-adaptive Telegram assistant platform that grows smarter with every interaction. It utilizes exposed metadata and discovered user data to infer intent and provide proactive, personalized assistance - all while remaining privacy-compliant.

---

## Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Quick Start](#-quick-start)
- [Configuration](#-configuration)
- [Project Structure](#-project-structure)
- [How It Adapts](#-how-it-adapts)
- [Privacy & Compliance](#-privacy--compliance)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)

---

## Features

| Feature | Description |
|---|---|
| **Self-Adaptive Layer** | Reads metadata (chat type, user, links, timing) to evolve its user profile over time |
| **Metadata Awareness** | Infers intent from signals like recurring phrases, link domains, and interaction patterns |
| **Smart Bot Layer** | Integrates with the official Telegram Bot API for fully automated workflows |
| **Contextual Memory** | Structured context records + long-term memory keyed by user and chat |
| **Intent Engine** | Advanced logic (rules + LLM) that conditions interpretation on history and metadata |
| **Privacy-By-Design** | Built-in opt-in mechanisms, data minimization, GDPR/CCPA tooling |
| **Multi-Account Ready** | Modular architecture supporting bot + user-client + task engine stacks |
| **Task Automation** | Cron-style and event-driven task scheduler with reminder and alert support |
| **AI-Powered Responses** | OpenAI GPT integration for context-aware, personalized reply generation |

---

## Architecture

The platform is divided into a clean modular core:

```
telegram-ultimate-platform/
  app.py              <-- Main Event Handler / Router
  core/
    ai.py             <-- AIEngine (OpenAI GPT integration)
    context.py        <-- Context extraction & metadata learning
    db.py             <-- Database layer (Postgres/SQLite)
    intent.py         <-- Intent handling & user profiling
    privacy.py        <-- Consent management & data rights
    tasks.py          <-- TaskManager: scheduling & reminders
  public/
    index.html        <-- Live demo UI
```

---

## Quick Start

### Prerequisites
- Python 3.10+
- PostgreSQL (or SQLite for dev)
- A Telegram Bot Token from [@BotFather](https://t.me/BotFather)
- (Optional) OpenAI API key for AI features

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/hakunaTgl/telegram-ultimate-platform.git
cd telegram-ultimate-platform

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
# Edit .env with your tokens and database URL

# 5. Initialize the database
python -c "from core.db import init_db; import asyncio; asyncio.run(init_db())"

# 6. Run the bot
python app.py
```

---

## Configuration

Copy `.env.example` to `.env` and fill in the required values:

```env
# Required
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
DATABASE_URL=postgresql://user:password@localhost/telegram_platform

# Optional - AI Features
OPENAI_API_KEY=your_openai_api_key_here
AI_MODEL=gpt-4-turbo-preview

# Optional - App Config
LOG_LEVEL=INFO
ALLOW_LIST=
MAX_CONTEXT_LENGTH=20
```

---

## Project Structure

```
telegram-ultimate-platform/
|-- app.py                  # Main entry point & Telegram handler
|-- requirements.txt        # Python dependencies
|-- .env.example            # Environment variable template
|-- schema.sql              # Database schema
|-- core/
|   |-- __init__.py         # Module init with version info
|   |-- ai.py               # AIEngine: OpenAI-powered response generation
|   |-- context.py          # Context extraction & metadata learning
|   |-- db.py               # Database layer (Postgres/SQLite)
|   |-- intent.py           # Intent handling & user profile logic
|   |-- privacy.py          # Consent management & data rights
|   `-- tasks.py            # TaskManager: scheduling & reminders
`-- public/
    `-- index.html          # Live demo UI
```

---

## How It Adapts

The platform builds a **per-user profile** by passively observing interaction patterns:

1. **Preference Learning** - Tracks user preferences (summaries, tasks, event extractions) and stores them in structured metadata.
2. **Chat Tagging** - Identifies "task spaces" or "event channels" based on message content and frequency.
3. **Persona Building** - Develops per-space personas (e.g., knowledge assistant vs. task summarizer) that shape the AI's tone.
4. **Temporal Context** - Message timing patterns (morning check-ins, late-night requests) inform scheduling and urgency detection.

---

## Privacy & Compliance

Privacy is a first-class citizen in this platform:

- **Opt-in required** - Personalization only activates after explicit user agreement.
- **Data Rights commands:**
  - `/forget_me` - Permanently deletes all stored data for the requesting user.
  - `/export_me` - Exports all stored data in JSON format (GDPR Article 20).
  - `/privacy` - Displays current data collection status and consent settings.
- **Data Minimization** - Only metadata inferred from interactions is stored; raw messages are never persisted.
- **Audit Logging** - All data access events are logged for compliance traceability.

---

## Roadmap

- [x] Core bot framework with Telegram Bot API
- [x] Metadata learning & intent engine
- [x] OpenAI GPT integration
- [x] Task scheduling & reminders
- [x] Privacy consent system
- [ ] Voice message transcription (Whisper API)
- [ ] Plugin system for custom command modules
- [ ] Web dashboard for analytics & user management
- [ ] Multi-language support (i18n)
- [ ] Docker Compose production deployment
- [ ] Webhook support (in addition to polling)

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m 'feat: add your feature'`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a Pull Request

Please read [CONTRIBUTING.md](.github/CONTRIBUTING.md) for code style guidelines.

---

## License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

<p align="center">Built with love by <a href="https://github.com/hakunaTgl">hakunaTgl (Tylor Fenwick)</a> - <a href="https://hakunatgl.github.io">Portfolio</a></p>
