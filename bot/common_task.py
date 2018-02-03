import logging

from .task import Task

log = logging.getLogger(__name__)


class CommonTask(Task):

    def __init__(self) -> None:
        super().__init__()
        self._strategies = []

    def run(self) -> None:
        for strategy in self._strategies:
            strategy.process()

    def __repr__(self) -> str:
        return "CommonTask(" \
               "strategies={}, " \
               "{})".format(self._strategies, super().__repr__())
