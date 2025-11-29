import os

# Telegram Bot API credentials
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Telegram User API credentials (from my.telegram.org)
API_ID = int(os.getenv("API_ID", "123456"))
API_HASH = os.getenv("API_HASH", "your_api_hash_here")

# Render port (default 10000)
PORT = int(os.getenv("PORT", "10000"))

# Storage paths
STORAGE_PATH = "./temp"
SESSION_PATH = "./sessions"
LOG_PATH = "./logs"
