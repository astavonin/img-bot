from abc import ABC
from typing import List

from data_provider import Media, Engine
from persistence import UsersStorage


class MediaSource(ABC):

    def __init__(self, data_provider: Engine = None):
        self._data_provider = data_provider

    def init(self, data_provider: Engine) -> None:
        self._data_provider = data_provider

    def get_media(self, pages: int) -> List[Media]:
        raise NotImplementedError()

    def __repr__(self) -> str:
        return f"MediaSource(" \
               f"data_provider={self._data_provider}, " \
               f")"


class Liker(ABC):

    def __init__(self, data_provider: Engine, persistence: UsersStorage):
        self._data_provider = data_provider
        self._persistence = persistence

    def init(self, data_provider: Engine, persistence: UsersStorage) -> None:
        self._data_provider = data_provider
        self._persistence = persistence

    def like_media(self, media: List[Media], count: int) -> int:
        raise NotImplementedError()

    def __repr__(self) -> str:
        return f"Liker(" \
               f"data_provider={self._data_provider}, " \
               f"persistence={self._persistence}" \
               f")"


class Commenter(ABC):

    def __init__(self, data_provider: Engine, persistence: UsersStorage):
        self._data_provider = data_provider
        self._persistence = persistence

    def init(self, data_provider: Engine, persistence: UsersStorage) -> None:
        self._data_provider = data_provider
        self._persistence = persistence

    def comment_media(self, media: List[Media], count: int) -> int:
        raise NotImplementedError()

    def __repr__(self) -> str:
        return f"Commenter(" \
               f"data_provider={self._data_provider}, " \
               f"persistence={self._persistence}" \
               f")"
