import logging
from enum import Enum

from data_provider import Engine
from persistence import UsersStorage
from strategy import MediaSource, Liker, Commenter

log = logging.getLogger(__name__)


class UsageStrategy(Enum):
    LIKE = 1
    COMMENT = 2
    FOLLOW = 3
    UNFOLLOW = 4


class Task:

    def __init__(self) -> None:
        super().__init__()

        self._engine = None
        self._user_storage = None
        self._like_srcs = []
        self._comment_srcs = []
        self._likers = []
        self._commenters = []

    def init(self, engine: Engine, user_storage: UsersStorage) -> None:
        self._engine = engine
        self._user_storage = user_storage

    def add_media_source(self, source: MediaSource, weight,
                         strategy: UsageStrategy) -> None:
        log.info(f"Registering new {source} with weight {weight} and strategy "
                 f"{strategy}")
        source.init(self._engine, self._user_storage)
        if strategy is UsageStrategy.LIKE:
            self._like_srcs.append((source, weight))
        elif strategy is UsageStrategy.COMMENT:
            self._comment_srcs.append((source, weight))
        else:
            raise NotImplementedError()

    def add_liker(self, liker: Liker) -> None:
        log.info(f"Registering new {liker}")
        liker.init(self._engine, self._user_storage)
        self._likers.append(liker)

    def add_commenter(self, commenter: Commenter) -> None:
        log.info(f"Registering new {commenter}")
        commenter.init(self._engine, self._user_storage)
        self._commenters.append(commenter)

    async def run(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Task(engine={self._engine}, " \
               f"user_storage={self._user_storage}, " \
               f"like_srcs={self._like_srcs}, " \
               f"comment_srcs={self._comment_srcs}, " \
               f"likers={self._likers}, " \
               f"commenters={self._commenters}" \
               f")"
