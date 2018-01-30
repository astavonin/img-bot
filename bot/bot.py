import logging
import threading
from datetime import timedelta
from time import sleep
from typing import List

from data_provider import Engine
from persistence import UsersStorage
from .task import Task

log = logging.getLogger(__name__)


class TaskExecution:

    def __init__(self, task, every) -> None:
        self.task = task
        self.every = every


def gen_delay(tasks: List[TaskExecution], max_delay=None) -> (float, List[Task]):
    total_wait = 0
    while max_delay is None or total_wait < max_delay:
        deltas = []
        for t in tasks:
            task_delay = t.every - (total_wait - (int(total_wait / t.every) * t.every))
            deltas.append((task_delay, t))
        wait, _ = min(deltas, key=lambda delay: delay[0])
        task_list = [delta[1].task for delta in deltas if delta[0] == wait]
        total_wait += wait
        yield wait, task_list


class Bot:
    def __init__(self, engine: Engine, persistence: UsersStorage) -> None:
        super().__init__()
        self._engine = engine
        self._persistence = persistence
        self._tasks = []

    def add_task(self, task: Task, every: timedelta) -> None:
        task.init(self._engine, self._persistence)
        self._tasks.append(TaskExecution(task, every.total_seconds()))

    def run(self) -> None:
        while True:
            for sleep_time, tasks in gen_delay(self._tasks):
                for task in tasks:
                    try:
                        job = threading.Thread(target=task.run)
                        job.start()
                    except Exception as ex:
                        log.error(f"Error: {ex}")
                log.info("{} tasks were executed. Will sleep for {} before next run"
                         .format(len(tasks), timedelta(seconds=sleep_time)))
                sleep(sleep_time)

    def __repr__(self) -> str:
        return f"Bot(" \
               f"engine={self._engine}, " \
               f"persistence={self._persistence}, " \
               f"comment_srcs={self._tasks}, " \
               f")"
