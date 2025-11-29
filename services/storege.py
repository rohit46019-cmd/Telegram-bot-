import os
from config import STORAGE_PATH

def ensure_dirs():
    os.makedirs(STORAGE_PATH, exist_ok=True)

def file_path(name: str) -> str:
    ensure_dirs()
    return os.path.join(STORAGE_PATH, name)
