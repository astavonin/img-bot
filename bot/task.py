import logging
from abc import ABC

from data_provider import Engine
from strategy import Strategy

log = logging.getLogger(__name__)


class Task(ABC):

    def __init__(self) -> None:
        super().__init__()

        self._engine = None
        self._user_storage = None
        self._strategies = []

    def init(self, engine: Engine) -> None:
        self._engine = engine
        for strategy in self._strategies:
            strategy.init(self._engine)

    def add_strategy(self, strategy: Strategy) -> None:
        log.info(f"Registering new {strategy}")
        self._strategies.append(strategy)

    def run(self) -> None:
        raise NotImplementedError()

    def __repr__(self) -> str:
        return f"Task(" \
               f"engine={self._engine}, " \
               f"strategies={self._strategies}" \
               f")"
