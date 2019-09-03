import logging
import threading

from data_provider import Engine
from .task import Task

log = logging.getLogger(__name__)


class Bot:
    def __init__(self, engine: Engine) -> None:
        super().__init__()
        self._engine = engine
        self._tasks = []

    def add_task(self, task: Task) -> None:
        task.init(self._engine)
        self._tasks.append(task)

    def run(self) -> None:
        jobs = []
        for task in self._tasks:
            try:
                log.info(f"Executing task {task}")
                job = threading.Thread(target=task.run)
                job.start()
                jobs.append(job)
            except Exception as ex:
                log.error(f"Error: {ex}")
        for job in jobs:
            job.join()

    def __repr__(self) -> str:
        return f"Bot(" \
               f"engine={self._engine}, " \
               f"tasks={self._tasks}, " \
               f")"
