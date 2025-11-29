import asyncio
from typing import Callable

async def with_backoff(func: Callable, *args, **kwargs):
    retry = 0
    while True:
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            retry += 1
            delay = min(30, 2 ** retry)
            await asyncio.sleep(delay)
