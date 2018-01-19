import logging
from datetime import timedelta, time

import persistence
from .task import Task
from data_provider import Engine

log = logging.getLogger(__name__)


class Bot:
    def __init__(self, engine: Engine) -> None:
        super().__init__()
        self._engine = engine
        self._user_storage = persistence.UsersStorage()
        self._tasks = []

    def add_task(self, task: Task, every: timedelta = None, at: time = None) -> None:
        if every is not None:
            self._tasks.append((every, task))
        elif at is not None:
            self._tasks.append((at, task))
        else:
            raise ValueError("`timedelta` or `at` should be provided!")

    def run(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Bot(engine = {self._engine}, " \
               f"like_srcs={self._user_storage}, " \
               f"comment_srcs={self._tasks}, " \
               f")"
