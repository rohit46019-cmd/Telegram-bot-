from typing import Optional

def apply_rename(original: str, tag: Optional[str]) -> str:
    if not tag:
        return original
    return f"{tag}_{original}"

def apply_text_filters(text: str, replace_map: dict, remove_list: list) -> str:
    out = text
    for k, v in (replace_map or {}).items():
        out = out.replace(k, v)
    for r in (remove_list or []):
        out = out.replace(r, "")
    return out
