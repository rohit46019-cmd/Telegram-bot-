# Placeholder for Pyrogram client lifecycle per user.
# Extend: maintain per-user sessions in ./sessions/{user_id}.session
# Load with Client(session_name, api_id=API_ID, api_hash=API_HASH)
# Provide get_client(user_id) that returns a connected Pyrogram Client.
from typing import Optional

def get_client(user_id: int) -> Optional[object]:
    # TODO: implement real Pyrogram session retrieval
    return None