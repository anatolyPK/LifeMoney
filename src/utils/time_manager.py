import time


def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Функция {func.__name__!r} выполнялась {end_time - start_time:.4f} секунд.")
        return result
    return wrapper
