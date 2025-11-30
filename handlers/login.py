from aiogram import Dispatcher
from aiogram.types import Message
from config import API_ID, API_HASH, SESSION_PATH
import os

# Temporary state storage
_login_state = {}


def register_login(dp: Dispatcher):

    @dp.message_handler(commands=["login"])
    async def login(m: Message):
        uid = m.from_user.id
        session_file = os.path.join(SESSION_PATH, str(uid))

        # Step 1: Ask user for phone number
        _login_state[uid] = {"step": "phone", "session_file": session_file}
        await m.answer("Send your mobile 📲 number with country code (e.g., +91xxxxxxxxxx)")

    @dp.message_handler(lambda m: _login_state.get(m.from_user.id, {}).get("step") == "phone")
    async def handle_phone(m: Message):
        # Import Pyrogram here (after event loop exists)
        from pyrogram import Client

        uid = m.from_user.id
        phone = m.text.strip()
        session_file = _login_state[uid]["session_file"]

        client = Client(session_file, api_id=API_ID, api_hash=API_HASH)
        await client.connect()

        # Send code and save phone_code_hash
        sent_code = await client.send_code(phone)

        _login_state[uid].update({
            "step": "otp",
            "client": client,
            "phone": phone,
            "hash": sent_code.phone_code_hash  # <--- important!
        })
        await m.answer("Enter the OTP you received 🔑")

    @dp.message_handler(lambda m: _login_state.get(m.from_user.id, {}).get("step") == "otp")
    async def handle_otp(m: Message):
        uid = m.from_user.id
        otp = m.text.strip()
        client = _login_state[uid]["client"]
        phone = _login_state[uid]["phone"]
        phone_hash = _login_state[uid]["hash"]

        try:
            await client.sign_in(phone_number=phone, phone_code_hash=phone_hash, phone_code=otp)
            _login_state[uid] = {"step": "done"}
            await m.answer("Login successful ✅")
        except Exception as e:
            await m.answer(f"Login failed ❌: {e}")

    @dp.message_handler(commands=["logout"])
    async def logout(m: Message):
        uid = m.from_user.id

        # Clean up session files
        session_file = os.path.join(SESSION_PATH, str(uid))
        for suffix in ["", ".session", ".session-journal"]:
            path = session_file + suffix
            if os.path.exists(path):
                os.remove(path)

        _login_state.pop(uid, None)
        await m.answer("Logged out ✅\nYour session files have been removed.")