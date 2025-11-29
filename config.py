import os

# Bot API token (from BotFather)
BOT_TOKEN = os.getenv("BOT_TOKEN", "REPLACE_ME")

# User API credentials (from my.telegram.org) for Pyrogram
API_ID = int(os.getenv("API_ID", "123456"))
API_HASH = os.getenv("API_HASH", "REPLACE_ME")

# Render listening port
PORT = int(os.getenv("PORT", "10000"))

# Storage paths
STORAGE_PATH = os.getenv("STORAGE_PATH", "./temp")
SESSION_PATH = os.getenv("SESSION_PATH", "./sessions")
LOG_PATH = os.getenv("LOG_PATH", "./logs")

# Feature toggles
ENABLE_TELEGRAM_USER_DOWNLOADS = True  # when true, extend downloader/uploader to use Pyrogram sessions
MAX_BATCH_ITEMS = int(os.getenv("MAX_BATCH_ITEMS", "500"))