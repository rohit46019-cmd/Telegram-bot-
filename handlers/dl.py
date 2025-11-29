import asyncio
from aiogram import Dispatcher
from aiogram.types import Message
from utils.progress import render_dl_bar
from services.uploader import upload_with_progress, STREAM
from services.downloader import download_website

def register_dl(dp: Dispatcher):
    user_waiting_link = set()

    @dp.message_handler(commands=["dl"])
    async def dl_command(m: Message):
        user_waiting_link.add(m.from_user.id)
        await m.answer("Send the link 🔗 you want to download.")

    @dp.message_handler(lambda msg: msg.from_user and msg.from_user.id in user_waiting_link and msg.text and msg.text.startswith("http"))
    async def dl_link(m: Message):
        uid = m.from_user.id
        user_waiting_link.discard(uid)
        url = m.text

        # Per-file download bar message (created once, edited in progress hook)
        dl_msg = await m.answer("Preparing download...")

        def progress_hook(d):
            if d.get('status') == 'downloading':
                done = int(d.get('downloaded_bytes', 0) or 0)
                total = int(d.get('total_bytes', d.get('total_bytes_estimate', 1)) or 1)
                speed = float(d.get('speed', 0.0)) / 1024 / 1024
                eta = int(d.get('eta', 0))
                txt = render_dl_bar(done, total, speed, eta)
                asyncio.create_task(dl_msg.edit_text(txt))
            elif d.get('status') == 'finished':
                asyncio.create_task(dl_msg.edit_text("Download complete ✅"))

        try:
            path, info = download_website(url, progress_hook)
        except Exception as e:
            await dl_msg.edit_text(f"Download failed: {e}")
            return

        # Delete download bar
        await dl_msg.delete()

        # Upload with streaming when video formats detected (simple heuristic)
        await upload_with_progress(m.bot, m.chat.id, path, reply_to_message_id=m.message_id, method=STREAM)
