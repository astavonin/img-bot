import logging
from abc import ABC

from data_provider import Engine
from persistence import UsersStorage

log = logging.getLogger(__name__)


class Task(ABC):

    def __init__(self) -> None:
        super().__init__()

        self._engine = None
        self._user_storage = None

    def init(self, engine: Engine, user_storage: UsersStorage) -> None:
        self._engine = engine
        self._user_storage = user_storage

    def run(self) -> None:
        raise NotImplementedError()

    def __repr__(self) -> str:
        return f"Task(" \
               f"engine={self._engine}, " \
               f"user_storage={self._user_storage}" \
               f")"
