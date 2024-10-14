from typing import Coroutine

from backend.src.modules.stocks.pricer import set_actual_stock_price


def get_stock_tasks() -> list[Coroutine]:
    tasks = []
    tasks.append(set_actual_stock_price)
    return tasks
