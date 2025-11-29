from aiogram import Bot
from utils.progress import render_ul_bar
import asyncio
import os

# Upload methods
PROGRAM_V2 = "program_v2"
SPYLIB_V1 = "spylib_v1"
AUTO = "auto"
DIRECT = "direct"
STREAM = "stream"

async def upload_with_progress(bot: Bot, chat_id: int, path: str, reply_to_message_id=None, method=AUTO):
    size = os.path.getsize(path)
    # Emit a simple per-file upload bar (simulated; Telegram doesn't expose upload progress)
    # For realism, we chunk-sleep to animate bar.
    total = max(size, 1)
    done = 0
    ul_msg = await bot.send_message(chat_id, render_ul_bar(0, total, 0.0, 0))
    # Choose upload method
    if method in (DIRECT, SPYLIB_V1):
        await bot.send_document(chat_id, open(path, "rb"), reply_to_message_id=reply_to_message_id)
    else:
        # STREAM, PROGRAM_V2, AUTO default to video if extension indicates video, else document.
        ext = os.path.splitext(path)[1].lower()
        if ext in [".mp4", ".mkv", ".webm", ".mov"]:
            await bot.send_video(chat_id, open(path, "rb"), supports_streaming=True, reply_to_message_id=reply_to_message_id)
        else:
            await bot.send_document(chat_id, open(path, "rb"), reply_to_message_id=reply_to_message_id)
    # Delete per-file upload bar after completion
    await ul_msg.delete()
