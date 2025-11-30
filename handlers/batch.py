import time
from aiogram import Dispatcher
from aiogram.types import Message
from utils.links import parse_link
from utils.progress import render_global_bar, render_dl_bar
from services.auth import is_logged_in
from config import MAX_BATCH_ITEMS

def register_batch(dp: Dispatcher):
    # Track user state and retry counts
    user_state = {}

    @dp.message_handler(commands=["batch"])
    async def batch(m: Message):
        uid = m.from_user.id
        if not is_logged_in(uid):
            await m.answer("Please /login first.")
            return

        user_state[uid] = {"step": "await_link", "retry": 0}
        await m.answer("Send the starting link 🔗 for Bulk download (e.g., https://t.me/c/3333627204/54)")

    @dp.message_handler(lambda msg: msg.from_user and msg.from_user.id in user_state and user_state[msg.from_user.id].get("step") == "await_link")
    async def batch_link(m: Message):
        uid = m.from_user.id
        parsed = parse_link(m.text)

        if not parsed:
            # Increment retry count
            user_state[uid]["retry"] += 1
            retries = user_state[uid]["retry"]

            if retries < 3:
                await m.answer(f"Invalid link ❌. You have {3 - retries} tries left. Send a valid Telegram message link.")
                return
            else:
                # Terminate command after 3 wrong attempts
                user_state.pop(uid, None)
                await m.answer("Too many invalid attempts ❌. Please start /batch again.")
                return

        # Valid link
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

        st = user_state.pop(uid)
        chat_ref = st["chat_ref"]
        start_id = st["start_id"]

        # Create pinned global bar
        global_msg = await m.answer(render_global_bar(0, count, 0.0, 0, f"https://t.me/c/{chat_ref}/{start_id}"))
        try:
            await global_msg.pin()
        except:
            pass

        # Simulated download loop (replace with real Pyrogram download)
        avg_speed = 2.5
        for i in range(count):
            current_id = start_id + i
            await global_msg.edit_text(render_global_bar(i, count, avg_speed, max(0, (count - i) * 2), f"https://t.me/c/{chat_ref}/{current_id}"))

            # Per-file download bar simulation
            done = 0
            total = 15 * 1024 * 1024
            dl_msg = await m.answer(render_dl_bar(done, total, avg_speed, 10))
            for _ in range(5):
                time.sleep(0.4)
                done += total // 5
                await dl_msg.edit_text(render_dl_bar(done, total, avg_speed, max(0, 10 - (_ + 1) * 2)))
            await dl_msg.delete()

            # Per-file upload simulation
            ul_msg = await m.answer("Uploading...")
            await m.bot.send_document(m.chat.id, ("demo.txt", b"demo content"))  # replace with real file
            await ul_msg.delete()

            # Update global progress
            await global_msg.edit_text(render_global_bar(i + 1, count, avg_speed, max(0, (count - i - 1) * 2), f"https://t.me/c/{chat_ref}/{current_id}"))

        # Finish
        try:
            await global_msg.delete()
        except:
            pass
        await m.answer(f"✅ Batch finished. {count} files delivered.")