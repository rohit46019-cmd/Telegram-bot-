def render_global_bar(done: int, total: int, avg_speed_mb: float, eta_s: int, current_link: str) -> str:
    pct = (done / total) * 100 if total else 0.0
    return f"""╭────────────────────────╮
│   Batch Progress (Pinned)
├────────────────────────
│ Files: {done}/{total}  ({pct:.1f}%)
│ Speed: {avg_speed_mb:.2f} MB/s
│ ETA: {eta_s}s
│ Current: {current_link}
╰────────────────────────╯"""

def render_dl_bar(done_bytes: int, total_bytes: int, speed_mb_s: float, eta_s: int) -> str:
    width = 10
    pct = (done_bytes / total_bytes) if total_bytes else 0.0
    fill = min(width, int(pct * width))
    bar = "♦" * fill + "·" * (width - fill)
    return f"""╭─────────────────────╮
│ Downloading...
├─────────────────────
│ {bar}
│ Completed: {done_bytes/1024/1024:.2f} MB/{(total_bytes or 1)/1024/1024:.2f} MB
│ Speed: {speed_mb_s:.2f} MB/s
│ ETA: {eta_s}s
╰─────────────────────╯"""

def render_ul_bar(done_bytes: int, total_bytes: int, speed_mb_s: float, eta_s: int) -> str:
    width = 10
    pct = (done_bytes / total_bytes) if total_bytes else 0.0
    fill = min(width, int(pct * width))
    bar = "▓" * fill + "·" * (width - fill)
    return f"""╭─────────────────────╮
│ Uploading...
├─────────────────────
│ {bar}
│ Completed: {done_bytes/1024/1024:.2f} MB/{(total_bytes or 1)/1024/1024:.2f} MB
│ Speed: {speed_mb_s:.2f} MB/s
│ ETA: {eta_s}s
╰─────────────────────╯"""
