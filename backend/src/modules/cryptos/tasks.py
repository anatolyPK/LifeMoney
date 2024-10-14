from typing import Coroutine

from backend.src.modules.cryptos.crypto.pricer import set_actual_crypto_price


def get_crypto_tasks() -> list[Coroutine]:
    tasks = []
    tasks.append(set_actual_crypto_price)
    return tasks
