import time
import asyncio
from functools import wraps


def timing_decorator(func):
    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)
        end_time = time.time()
        print(
            f"Функция {func.__name__!r} выполнялась {end_time - start_time:.4f} секунд."
        )
        return result

    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(
            f"Функция {func.__name__!r} выполнялась {end_time - start_time:.4f} секунд."
        )
        return result

    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper
