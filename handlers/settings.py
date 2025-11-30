from aiogram import Dispatcher, types
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

def settings_keyboard():
    kb = InlineKeyboardMarkup(row_width=3)
    kb.add(
        InlineKeyboardButton("Set chat id", callback_data="set_chat"),
        InlineKeyboardButton("Set rename tag", callback_data="set_rename"),
        InlineKeyboardButton("Caption", callback_data="set_caption"),
        InlineKeyboardButton("Replace word", callback_data="replace_word"),
        InlineKeyboardButton("Remove word", callback_data="remove_word"),
        InlineKeyboardButton("Reset", callback_data="reset"),
        InlineKeyboardButton("Session login", callback_data="session_login"),
        InlineKeyboardButton("Set thumbnail", callback_data="set_thumb"),
        InlineKeyboardButton("Upload method", callback_data="upload_method"),
    )
    return kb

def register_settings(dp: Dispatcher):
    # /settings command
    @dp.message_handler(commands=["settings"])
    async def settings(m: Message):
        await m.answer("Settings:", reply_markup=settings_keyboard())

    # Callback handlers for each button
    @dp.callback_query_handler(lambda c: c.data == "set_chat")
    async def cb_set_chat(c: types.CallbackQuery):
        await c.answer("You tapped: Set chat id ✅")

    @dp.callback_query_handler(lambda c: c.data == "set_rename")
    async def cb_set_rename(c: types.CallbackQuery):
        await c.answer("You tapped: Set rename tag ✅")

    @dp.callback_query_handler(lambda c: c.data == "set_caption")
    async def cb_set_caption(c: types.CallbackQuery):
        await c.answer("You tapped: Caption ✅")

    @dp.callback_query_handler(lambda c: c.data == "replace_word")
    async def cb_replace_word(c: types.CallbackQuery):
        await c.answer("You tapped: Replace word ✅")

    @dp.callback_query_handler(lambda c: c.data == "remove_word")
    async def cb_remove_word(c: types.CallbackQuery):
        await c.answer("You tapped: Remove word ✅")

    @dp.callback_query_handler(lambda c: c.data == "reset")
    async def cb_reset(c: types.CallbackQuery):
        await c.answer("You tapped: Reset ✅")

    @dp.callback_query_handler(lambda c: c.data == "session_login")
    async def cb_session_login(c: types.CallbackQuery):
        await c.answer("You tapped: Session login ✅")

    @dp.callback_query_handler(lambda c: c.data == "set_thumb")
    async def cb_set_thumb(c: types.CallbackQuery):
        await c.answer("You tapped: Set thumbnail ✅")

    @dp.callback_query_handler(lambda c: c.data == "upload_method")
    async def cb_upload_method(c: types.CallbackQuery):
        await c.answer("You tapped: Upload method ✅")