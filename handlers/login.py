from aiogram import Dispatcher
from aiogram.types import Message
from services.auth import is_logged_in, set_logged_in

def register_login(dp: Dispatcher):
    @dp.message_handler(commands=["login"])
    async def login(m: Message):
        uid = m.from_user.id
        if is_logged_in(uid):
            await m.answer("You are already logged in ✅")
            return
        # Simplified flow: emulate login success (replace with Pyrogram phone/OTP/2FA)
        # Ask phone
        await m.answer("Send your mobile 📲 number with country code (e.g., +91xxxxxxxxxx)")
        # In real flow, capture next message, send_code, then ask for OTP and optional 2FA
        # Here we mark as logged-in for demo:
        set_logged_in(uid, True)
        await m.answer("Login successful ✅")

    @dp.message_handler(commands=["logout"])
    async def logout(m: Message):
        uid = m.from_user.id
        set_logged_in(uid, False)
        await m.answer("Logged out. Session cleared.")
