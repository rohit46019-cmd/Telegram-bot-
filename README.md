# Telegram Media Assistant Bot

Dual progress bars (global pinned + per-file), session login, batch downloads, website /dl, and a Render health-check server.

## Commands
- /start — Welcome message
- /login — Phone → OTP → optional 2FA
- /logout — Clear session
- Paste Telegram message link — Single download (if accessible)
- /batch — Bulk download from starting link; shows global pinned bar + per-file bars
- /cancel — Cancel batch
- /dl — Download from websites (yt-dlp), per-file bars
- /settings — Customize: chat id, rename tag, caption, replace/remove text, reset, session, thumbnail, upload method

## Edit these files
- config.py — BOT_TOKEN, API_ID, API_HASH, paths, PORT
- main.py — entry point + FastAPI health-check
- utils/progress.py — progress bar visuals
- services/uploader.py — upload methods
- services/downloader.py — Telegram downloads (extend to Pyrogram for private access)
- handlers/* — command handlers

## Render health-check
Main opens FastAPI on PORT so Render detects an open port while bot polls.

## Notes
This starter uses Bot API for sending files and yt-dlp for /dl. For private chats/channels, integrate Pyrogram sessions in services/tg_client.py and switch downloader/uploader to user sessions.# Telegram-bot-