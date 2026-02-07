# Telegram Ultimate Platform

A complete, self-adaptive Telegram assistant platform that grows smarter with every interaction. It utilizes exposed metadata and lawfully discovered user data to infer intent and provide proactive assistance.

## 🚀 Features

- **Self-Adaptive Layer**: Reads exposed metadata (chat type, user, links, timing) to evolve its profile.
- **Metadata Awareness**: Infers intent and root meaning from signals like recurring phrases, link domains, and interaction patterns.
- **Smart Bot Layer**: Sits on top of normal accounts and the official Bot API for advanced automation.
- **Contextual Memory**: Structured context records and long-term memory store keyed by user and chat.
- **Intent Engine**: Advanced logic (rules/LLM) that conditions interpretation on history and metadata.
- **Privacy-By-Design**: Built-in opt-in mechanisms, data minimization, and GDPR/CCPA compliance tools.
- **Multi-Account Ready**: Architected for modular bot + user-client + task engine stack.

## 🛠️ System Architecture

1. **Transport Layer**: Bot API integration using `python-telegram-bot`.
2. **Context Extractor**: Normalizes updates into structured metadata records.
3. **Memory Store**: Database-backed preference vectors and interaction logs.
4. **Adaptive Engine**: Intent detection conditioned on evolving memory.
5. **Privacy Layer**: Standard bot privacy policy enforcement and user controls.

## 📁 Project Structure

```text
.
├── app.py              # Main application entry point
├── core/               # Core system modules
│   ├── __init__.py     # Module initialization
│   ├── context.py      # Context & metadata extraction
│   ├── db.py           # Database & memory store layer
│   ├── intent.py       # Adaptive intent engine logic
│   └── privacy.py      # Privacy & consent handling
├── schema.sql          # Database schema (Postgres/SQLite)
├── requirements.txt    # Python dependencies
└── .env.example        # Configuration template
```

## 🚥 Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/hakunaTgl/telegram-ultimate-platform.git
   cd telegram-ultimate-platform
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment:**
   Copy `.env.example` to `.env` and add your `TELEGRAM_BOT_TOKEN` and `DATABASE_URL`.

4. **Initialize Database:**
   ```bash
   # Run the schema.sql in your Postgres/SQLite database
   ```

5. **Run the bot:**
   ```bash
   python app.py
   ```

## 🧠 How it Adapts

- **Preference Learning**: Automatically tracks if you like summaries, tasks, or event extractions.
- **Chat Tagging**: Automatically identifies "task spaces" or "event channels" based on content.
- **Persona Building**: Develops a per-space persona (e.g., knowledge assistant in DMs, summarizer in channels).

## 🛡️ Privacy & Compliance

This system is built with transparency in mind:
- **Opt-in required**: Users must explicitly agree to personalization.
- **Data Rights**: Commands for `/forget_me` (deletion) and `/export_me` (access) are built-in.
- **Minimization**: Only stores metadata necessary for personalization.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
