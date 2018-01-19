from typing import List

from data_provider import Engine, Media
from persistence import UsersStorage
from strategy import Liker, Commenter


class FakeLiker(Liker):

    def init(self, data_provider: Engine, persistence: UsersStorage) -> None:
        pass

    def like_media(self, media: List[Media], count: int) -> int:
        pass


class FakeCommenter(Commenter):
    def init(self, data_provider: Engine, persistence: UsersStorage) -> None:
        pass

    def comment_media(self, media: List[Media], count: int) -> int:
        pass
