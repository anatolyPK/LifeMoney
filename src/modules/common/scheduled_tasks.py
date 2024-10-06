import asyncio
from typing import Coroutine


class ScheduledTasks:
    def __init__(self, interval_sec: int):
        self.interval = interval_sec
        self._running = False
        self._tasks = []

    def add_tasks(self, coro: list[Coroutine]):
        self._tasks.extend(coro)

    def remove_task(self, coro):
        if coro in self._tasks:
            self._tasks.remove(coro)

    async def run_tasks(self):
        self._running = True
        while self._running:
            print('LOOPOOOOPP')
            await asyncio.sleep(self.interval)
            try:
                await asyncio.gather(
                    *(task() for task in self._tasks),
                    return_exceptions=True
                )
            except Exception as e:
                print(f"An error occurred: {e}")
            for task in self._tasks:
                if isinstance(task, asyncio.Future) and task.done() and task.exception() is not None:
                    print(f"Task raised an exception: {task.exception()}")

    def close(self):
        self._running = False
