import os
import asyncio
from aiogram import Dispatcher
from aiogram.types import Message
from pyrogram.errors import RPCError
from utils.links import parse_link
from utils.progress import render_global_bar, render_dl_bar
from services.auth import is_logged_in, get_client
from config import MAX_BATCH_ITEMS, TEMP_DOWNLOAD_PATH

def register_batch(dp: Dispatcher):
    """Register /batch command handlers."""
    user_state = {}  # Track user state per chat

    @dp.message_handler(commands=["batch"])
    async def batch_start(m: Message):
        uid = m.from_user.id
        if not is_logged_in(uid):
            await m.answer("Please /login first.")
            return

        user_state[uid] = {"step": "await_link", "retry": 0}
        await m.answer("Send the starting link 🔗 for bulk download (e.g., https://t.me/c/3333627204/54)")

    @dp.message_handler(lambda msg: msg.from_user and msg.from_user.id in user_state and user_state[msg.from_user.id].get("step") == "await_link")
    async def batch_link(m: Message):
        uid = m.from_user.id
        parsed = parse_link(m.text)

        if not parsed:
            # Retry logic
            user_state[uid]["retry"] += 1
            retries = user_state[uid]["retry"]
            if retries < 3:
                await m.answer(f"Invalid link ❌. You have {3 - retries} tries left. Send a valid Telegram message link.")
            else:
                user_state.pop(uid, None)
                await m.answer("Too many invalid attempts ❌. Please start /batch again.")
            return

        chat_ref, start_msg_id = parsed
        user_state[uid].update({"step": "await_count", "chat_ref": chat_ref, "start_id": start_msg_id})
        await m.answer("How many messages do you want to download? (e.g., 300)")

    @dp.message_handler(lambda msg: msg.from_user and msg.from_user.id in user_state and user_state[msg.from_user.id].get("step") == "await_count")
    async def batch_count(m: Message):
        uid = m.from_user.id
        try:
            count = int(m.text.strip())
        except:
            await m.answer("Please send a valid number.")
            return

        if count <= 0 or count > MAX_BATCH_ITEMS:
            await m.answer(f"Please choose between 1 and {MAX_BATCH_ITEMS}.")
            return

        # Get user state and Pyrogram client
        st = user_state.pop(uid)
        chat_ref = st["chat_ref"]
        start_id = st["start_id"]
        client = get_client(uid)  # get_client should return Pyrogram Client for the logged-in user

        if not client:
            await m.answer("Your session is missing. Please /login again.")
            return

        # Ensure temp folder exists
        os.makedirs(TEMP_DOWNLOAD_PATH, exist_ok=True)

        # Global progress message
        global_msg = await m.answer(render_global_bar(0, count, 0.0, 0, f"https://t.me/c/{chat_ref}/{start_id}"))
        try:
            await global_msg.pin()
        except:
            pass

        for i in range(count):
            current_id = start_id + i
            try:
                # Fetch the message
                msg_obj = await client.get_messages(chat_id=chat_ref, message_ids=current_id)
                if msg_obj and msg_obj.media:
                    file_path = await client.download_media(msg_obj, file_name=os.path.join(TEMP_DOWNLOAD_PATH, f"{current_id}"))
                else:
                    file_path = None
            except RPCError as e:
                await m.answer(f"Failed to download message {current_id}: {e}")
                file_path = None

            # Update global progress
            await global_msg.edit_text(render_global_bar(i, count, 1.0, max(0, (count - i) * 2), f"https://t.me/c/{chat_ref}/{current_id}"))

            # Upload to user if downloaded
            if file_path:
                ul_msg = await m.answer("Uploading...")
                await m.bot.send_document(m.chat.id, file_path)
                await ul_msg.delete()
                os.remove(file_path)  # Clean up

        # Finish
        try:
            await global_msg.delete()
        except:
            pass
        await m.answer(f"✅ Batch finished. {count} files delivered.")