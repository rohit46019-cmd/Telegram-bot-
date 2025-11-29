from aiogram import Dispatcher
from aiogram.types import Message

def register_start(dp: Dispatcher):
    @dp.message_handler(commands=["start"])
    async def start(m: Message):
        await m.answer("Welcome 😊 Bot is live.\nUse /login to connect your account.\nSend a Telegram message link to download a single file.\nTry /batch or /dl for bulk/website downloads.")
