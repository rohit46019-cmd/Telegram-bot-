from aiogram import Dispatcher
from aiogram.types import Message
from utils.links import parse_link
from services.auth import is_logged_in

def register_single(dp: Dispatcher):
    @dp.message_handler(lambda msg: msg.text and msg.text.startswith("http"))
    async def auto_single(m: Message):
        parsed = parse_link(m.text)
        if not parsed:
            return  # let /dl handler take website links
        uid = m.from_user.id
        if not is_logged_in(uid):
            await m.answer("Please /login first to access Telegram content.")
            return
        chat_ref, msg_id = parsed
        # TODO: call services.downloader.download_telegram_message and then upload result
        await m.answer(f"Detected Telegram message link.\nChat: {chat_ref}\nMessage ID: {msg_id}\n(Implement Pyrogram download for private content.)")
