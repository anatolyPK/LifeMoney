from modules.cryptos.tasks import get_crypto_tasks
from modules.stocks.tasks import get_stock_tasks


def get_async_tasks():
    stock_tasks = get_stock_tasks()
    crypto_tasks = get_crypto_tasks()
    tasks = [
        *stock_tasks,
        *crypto_tasks,
    ]
    return tasks