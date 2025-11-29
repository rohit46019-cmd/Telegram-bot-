# Minimal login state tracking using memory dict.
# For production, use a DB or Redis.
from typing import Dict

_login_state: Dict[int, bool] = {}

def is_logged_in(user_id: int) -> bool:
    return _login_state.get(user_id, False)

def set_logged_in(user_id: int, flag: bool):
    _login_state[user_id] = flag
