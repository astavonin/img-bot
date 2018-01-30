import logging
import shelve
from enum import Enum
from typing import Set

from data_provider import Engine, User

log = logging.getLogger(__name__)


class PersistReason(Enum):
    WHITE_LIST = 0
    STOP_WORD = 1
    TOO_MANY_FOLLOWERS = 2
    TOO_MANY_FOLLOWING = 3
    BAD_FOLLOW_RATIO = 4


class PersistedUser:

    def __key(self):
        return self.user_id, self.reason

    def __init__(self, user_id, reason) -> None:
        self.user_id = user_id
        self.reason = reason

    def __hash__(self) -> int:
        return hash(self.__key())

    def __eq__(self, o: object) -> bool:
        return (isinstance(o, self.__class__) and
                self.__key() == o.__key())


class UsersStorage:

    def _load_from_storage(self, name) -> Set[PersistedUser]:
        with shelve.open(self._storage_path) as db:
            if name in db:
                return db[name]
            return set()

    def _store_to_storage(self, name, data: Set[PersistedUser]) -> None:
        with shelve.open(self._storage_path) as db:
            db[name] = data

    def __init__(self, storage_path) -> None:
        self._storage_path = storage_path
        self._blacklist = self._load_from_storage("black_list")
        self._whitelist = self._load_from_storage("white_list")

    def update_black_list(self, data_source: Engine):
        pass

    def add_to_blacklist(self, user: User, reason: PersistReason) -> None:
        log.info(f"Adding to blacklist {user} because of {reason}")
        self._blacklist.add(PersistedUser(user.id, reason))
        self._store_to_storage("black_list", self._blacklist)

    def add_to_whitelist(self, user: User) -> None:
        log.info(f"Adding to whitelist {user}")
        self._whitelist.add(PersistedUser(user.id, PersistReason.WHITE_LIST))
        self._store_to_storage("white_list", self._whitelist)

    def in_blacklist(self, user: User) -> bool:
        return user.id in self._blacklist

    def in_whitelist(self, user: User) -> bool:
        return user.id in self._whitelist
