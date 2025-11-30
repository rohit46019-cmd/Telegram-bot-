from aiogram import Dispatcher
from aiogram.types import Message
from config import API_ID, API_HASH, SESSION_PATH
import os
from services.auth import set_logged_in  # Import global login flag

# Temporary per-step state (memory dict)
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
        from pyrogram import Client
        from pyrogram.errors import PhoneCodeInvalid, PhoneCodeExpired

        uid = m.from_user.id
        phone = m.text.strip()
        session_file = _login_state[uid]["session_file"]

        client = Client(session_file, api_id=API_ID, api_hash=API_HASH)
        await client.connect()

        try:
            sent_code = await client.send_code(phone)
        except (PhoneCodeInvalid, PhoneCodeExpired) as e:
            await m.answer(f"Failed to send code ❌: {e}")
            return

        # Save OTP info and client
        _login_state[uid].update({
            "step": "otp",
            "client": client,
            "phone": phone,
            "hash": sent_code.phone_code_hash
        })
        await m.answer("Enter the OTP you received 🔑")

    @dp.message_handler(lambda m: _login_state.get(m.from_user.id, {}).get("step") == "otp")
    async def handle_otp(m: Message):
        from pyrogram.errors import SessionPasswordNeeded, PhoneCodeInvalid, PhoneCodeExpired

        uid = m.from_user.id
        otp = m.text.strip()
        client = _login_state[uid]["client"]
        phone = _login_state[uid]["phone"]
        phone_hash = _login_state[uid]["hash"]

        try:
            await client.sign_in(phone_number=phone, phone_code_hash=phone_hash, phone_code=otp)
            # Mark user as logged in globally
            set_logged_in(uid, True)
            _login_state[uid] = {"step": "done"}
            await m.answer("Login successful ✅")
        except SessionPasswordNeeded:
            _login_state[uid]["step"] = "2fa"
            await m.answer("This account has 2FA enabled 🔐\nPlease send your password:")
        except (PhoneCodeInvalid, PhoneCodeExpired) as e:
            await m.answer(f"OTP invalid/expired ❌: {e}")
        except Exception as e:
            await m.answer(f"Login failed ❌: {e}")

    @dp.message_handler(lambda m: _login_state.get(m.from_user.id, {}).get("step") == "2fa")
    async def handle_2fa(m: Message):
        from pyrogram.errors import PasswordHashInvalid

        uid = m.from_user.id
        password = m.text.strip()
        client = _login_state[uid]["client"]

        try:
            await client.check_password(password)
            # Mark user as logged in globally
            set_logged_in(uid, True)
            _login_state[uid] = {"step": "done"}
            await m.answer("Login successful ✅")
        except PasswordHashInvalid:
            await m.answer("Incorrect password ❌. Please try again.")
        except Exception as e:
            await m.answer(f"Login failed ❌: {e}")

    @dp.message_handler(commands=["logout"])
    async def logout(m: Message):
        uid = m.from_user.id
        session_file = os.path.join(SESSION_PATH, str(uid))

        # Remove session files
        for suffix in ["", ".session", ".session-journal"]:
            path = session_file + suffix
            if os.path.exists(path):
                os.remove(path)

        _login_state.pop(uid, None)
        set_logged_in(uid, False)  # Reset global login flag
        await m.answer("Logged out ✅\nYour session files have been removed.")