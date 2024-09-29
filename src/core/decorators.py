import time
from functools import wraps


def timeit(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        await func(*args, **kwargs)
        end_time = time.time()
        return end_time - start_time

    return wrapper
