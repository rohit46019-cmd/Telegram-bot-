import asyncio
import uvicorn
from fastapi import FastAPI
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from config import BOT_TOKEN, PORT
from handlers.start import register_start
from handlers.login import register_login
from handlers.single import register_single
from handlers.batch import register_batch
from handlers.cancel import register_cancel
from handlers.dl import register_dl
from handlers.settings import register_settings

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Register handlers
register_start(dp)
register_login(dp)
register_single(dp)
register_batch(dp)
register_cancel(dp)
register_dl(dp)
register_settings(dp)

# Health-check server for Render
app = FastAPI()


@app.get("/")
def read_root():
    return {"status": "ok", "message": "Bot is running"}


async def start_bot():
    """Start Aiogram bot polling."""
    await dp.start_polling()


def start_fastapi():
    """Start FastAPI server (runs in a separate thread)."""
    uvicorn.run(app, host="0.0.0.0", port=PORT)


async def main():
    # Run Aiogram bot inside event loop
    bot_task = asyncio.create_task(start_bot())

    # Run FastAPI server in a separate thread
    api_task = asyncio.to_thread(start_fastapi)

    await asyncio.gather(bot_task, api_task)


if __name__ == "__main__":
    asyncio.run(main())