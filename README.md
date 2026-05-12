# Burmese AI Roleplay Companion Telegram Bot 🤖🎭

An intelligent AI-powered Telegram bot for Burmese language roleplay and cultural conversations. Features dual AI providers (Claude + Groq), per-user memory management, and multiple engaging storylines.

## 🌟 Features

- ✅ **Dual AI Integration**: Claude 3.5 Sonnet (primary) + Groq Mixtral (fallback/free tier)
- ✅ **Per-User Memory**: Maintains conversation history (configurable storage)
- ✅ **Multiple Stories**: 3 unique Burmese roleplay scenarios
- ✅ **NSFW Toggle**: Switch content filtering on/off
- ✅ **Burmese Language Support**: Full Myanmar Unicode support
- ✅ **Memory Reset**: Automatic reset on story change or `/clear` command
- ✅ **Error Handling**: Graceful API fallback and user-friendly error messages
- ✅ **Simple Structure**: Easy to understand and modify

## 📦 Project Structure

```
transformer/
├── main.py              # Main bot application with command handlers
├── config.py            # Configuration and constants
├── user_manager.py      # Per-user memory and session management
├── story_manager.py     # Story and character database
├── ai_provider.py       # Dual AI API integration
├── requirements.txt     # Python dependencies (May 2026 latest)
├── .env.example         # Environment configuration template
├── .gitignore          # Git exclusions
├── stories.json        # Pre-loaded Burmese roleplay stories
├── Procfile            # Deployment configuration
└── README.md           # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Telegram account & BotFather token
- Anthropic API key (Claude) - Optional but recommended
- Groq API key (Free tier) - Optional fallback

### Step 1: Clone Repository

```bash
git clone https://github.com/koko-fanny/transformer.git
cd transformer
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment

```bash
# Copy example configuration
cp .env.example .env

# Edit .env with your keys
nano .env  # or use your preferred editor
```

**Required Environment Variables:**

```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_from_botfather
ANTHROPIC_API_KEY=your_claude_api_key_from_anthropic
GROQ_API_KEY=your_groq_api_key_from_groq_console
```

### Step 5: Run the Bot

```bash
python main.py
```

You should see:
```
2026-05-12 18:30:45,123 - __main__ - INFO - 🤖 Burmese AI Roleplay Bot Started...
```

## 🎮 Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Initialize bot and get welcome message |
| `/stories` | Select a roleplay story from available options |
| `/settings` | Manage preferences (NSFW mode, etc.) |
| `/clear` | Reset memory and current story |
| `/help` | Show help and usage guide |

## 📖 Available Stories

1. **Ma Su (မဆူ)** - Traditional Myanmar Culture Expert
   - Friendly discussions about Burmese culture and daily life
   - Perfect for learning about Myanmar traditions

2. **Daw Lin (ဒေါ် လင်)** - Wise Elder
   - Philosophical discussions about life and Buddhism
   - Share wisdom and cultural insights

3. **Ko Kyaw (ကို ကျော်)** - Traditional Healer
   - Information about traditional Burmese medicine
   - Natural remedies and wellness practices

## 🔑 Getting API Keys

### Anthropic (Claude)
1. Visit https://console.anthropic.com
2. Sign up or log in
3. Create API key in account settings
4. Copy to `.env` as `ANTHROPIC_API_KEY`

### Groq (Free Tier - Recommended)
1. Visit https://console.groq.com
2. Sign up with email
3. Create API key
4. Copy to `.env` as `GROQ_API_KEY`

### Telegram Bot Token
1. Open Telegram and search for `@BotFather`
2. Send `/newbot`
3. Follow prompts to create bot
4. Copy token to `.env` as `TELEGRAM_BOT_TOKEN`

## 🌐 Deployment Options

### Option 1: Railway (Recommended) ⭐

**Free tier: 500 hours/month**

```bash
# 1. Push code to GitHub
git push origin main

# 2. Connect at railway.app
# - Sign up with GitHub
# - Create new project
# - Connect GitHub repo
# - Add environment variables (.env)
# - Deploy automatically

# 3. Bot runs 24/7
```

### Option 2: Render.com

**Free tier: One active service**

```bash
# 1. Push to GitHub
# 2. Sign up at render.com
# 3. Create "Web Service"
# 4. Connect GitHub repo
# 5. Set environment variables
# 6. Deploy
```

### Option 3: Heroku (Legacy)

```bash
# 1. Install Heroku CLI
# 2. Login: heroku login
# 3. Create app: heroku create your-app-name
# 4. Set config: heroku config:set TELEGRAM_BOT_TOKEN=xxx
# 5. Deploy: git push heroku main
```

### Option 4: VPS (Advanced)

```bash
# On your VPS:
sudo apt update
sudo apt install python3-pip
git clone your-repo-url
cd transformer
pip install -r requirements.txt
cp .env.example .env
# Edit .env with keys
python main.py &  # Run in background
```

## 🧪 Testing Locally

```bash
# Test imports
python -c "import main; import config; import user_manager; import story_manager; import ai_provider; print('✅ All imports OK')"

# Test in Telegram
# - Start chat with your bot
# - Send /start
# - Try /help
# - Select /stories
# - Send a message and see response
```

## ⚙️ Configuration

Edit `config.py` to customize:

```python
MAX_TOKENS = 1024              # Response length limit
TEMPERATURE = 0.7              # AI creativity (0-1)
MAX_MEMORY_MESSAGES = 20       # Per-user memory size
NSFW_FILTER_PROMPT = "..."    # NSFW filter instructions
```

## 🔐 Security

- ✅ No hardcoded secrets (all in `.env`)
- ✅ `.gitignore` prevents accidental exposure
- ✅ Per-user isolated sessions
- ✅ Environment variables in `.env` (never commit!)
- ✅ User-friendly error messages

## 📊 Monitoring

Check bot logs:
```bash
# If running locally
# Logs appear in terminal

# On Railway/Render
# View logs in dashboard under "Logs" tab
```

## 🐛 Troubleshooting

### Bot doesn't respond
- ✅ Check `TELEGRAM_BOT_TOKEN` in `.env`
- ✅ Verify token with `@BotFather` on Telegram
- ✅ Check logs for errors

### No API responses
- ✅ Verify `ANTHROPIC_API_KEY` and `GROQ_API_KEY` in `.env`
- ✅ Check API quotas and billing
- ✅ Groq fallback should work if Claude fails

### Memory issues
- ✅ Reduce `MAX_MEMORY_MESSAGES` in config.py
- ✅ Use `/clear` to reset user memory

### Deployment issues
- ✅ Ensure `requirements.txt` is up to date
- ✅ Check Python version (3.10+)
- ✅ Verify all environment variables set

## 📝 Adding Custom Stories

Edit `stories.json`:

```json
{
  "id": "your_story_id",
  "name": "မြန်မာ အညွှန်း",
  "name_en": "English Name",
  "description": "မြန်မာ ဖော်ပြချက်",
  "system_prompt": "Your character personality and behavior...",
  "initial_message": "Starting message..."
}
```

## 🤝 Contributing

Contributions welcome! Areas to improve:
- Additional Burmese stories
- More language support
- Enhanced memory management
- UI improvements

## 📄 License

This project is open source and available for personal and educational use.

## 🎯 Future Enhancements

- [ ] Voice message support
- [ ] Image generation integration
- [ ] User profile persistence (database)
- [ ] Admin dashboard
- [ ] Multi-language support
- [ ] Advanced memory with semantic search
- [ ] User statistics and analytics

## 💬 Support

For issues and questions:
1. Check troubleshooting section above
2. Review code comments in Python files
3. Check logs for error messages
4. Open GitHub issue with details

## ✨ Acknowledgments

- Telegram Bot API
- Anthropic Claude AI
- Groq Mixtral AI
- Python Telegram Bot library

---

**Made with ❤️ for Burmese language lovers** 🇲🇲

Last updated: May 12, 2026 | Version: 1.0.0
