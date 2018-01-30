import logging

from data_provider import Engine
from persistence import UsersStorage
from strategy import MediaSource, Strategy

log = logging.getLogger(__name__)


class Task:

    def __init__(self) -> None:
        super().__init__()

        self._engine = None
        self._user_storage = None
        self._strategies = []
        self._media_source = []

    def init(self, engine: Engine, user_storage: UsersStorage) -> None:
        self._engine = engine
        self._user_storage = user_storage
        for strategy in self._strategies:
            strategy.init(self._engine, self._user_storage)
        for medias in self._media_source:
            medias.init(self._engine)

    def add_media_source(self, source: MediaSource) -> None:
        log.info(f"Registering new {source}")
        self._media_source.append(source)

    def add_strategy(self, strategy: Strategy):
        log.info(f"Registering new {strategy}")
        self._strategies.append(strategy)

    def run(self) -> None:
        medias = set()
        for src in self._media_source:
            medias = medias | set(src.get_media())
        log.info("Executing {} strategies on {} medias".format(len(self._strategies), len(medias)))
        media_list = list(medias)
        for strategy in self._strategies:
            strategy.process_media(media_list)

    def __repr__(self) -> str:
        return f"Task(" \
               f"engine={self._engine}, " \
               f"user_storage={self._user_storage}, " \
               f"media_source={self._media_source}, " \
               f"strategies={self._strategies}, " \
               f")"

# f"total_likes={self._total_likes}, "
