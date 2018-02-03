import logging
import shelve
from datetime import datetime
from enum import Enum
from typing import List

from data_provider.types import to_user_id

log = logging.getLogger(__name__)


class PersistReason(Enum):
    WHITE_LIST = 0
    STOP_WORD = 1
    TOO_MANY_FOLLOWERS = 2
    TOO_MANY_FOLLOWING = 3
    BAD_FOLLOW_RATIO = 4
    BOT = 5
    NOT_FOLLOWED = 6


class PersistedUser:

    def __key(self):
        return self.user_id

    def __init__(self, user_id, reason) -> None:
        self.user_id = user_id
        self.reason = reason

    def __hash__(self) -> int:
        return hash(self.__key())

    def __eq__(self, o: object) -> bool:
        return (isinstance(o, self.__class__) and
                self.__key() == o.__key())


class UserInteraction:

    def __init__(self, user_id, last_like=None) -> None:
        self.user_id = user_id
        self.last_like = last_like
        self.likes_attempt = 0


class UsersStorage:

    def _load_from_storage(self, name, def_container):
        with shelve.open(self._storage_path) as db:
            if name in db:
                return db[name]
            return def_container

    def _store_to_storage(self, name, data) -> None:
        with shelve.open(self._storage_path) as db:
            db[name] = data

    def __init__(self, storage_path) -> None:
        self._storage_path = storage_path
        self._blacklist = self._load_from_storage("black_list", set())
        self._whitelist = self._load_from_storage("white_list", set())
        self._interactions = self._load_from_storage("interactions", {})

    def add_to_blacklist(self, user, reason: PersistReason) -> None:
        log.info(f"Adding to blacklist {user} because of {reason}")
        self._blacklist.add(PersistedUser(to_user_id(user), reason))

    def add_to_whitelist(self, user) -> None:
        log.info(f"Adding to whitelist {user}")
        self._whitelist.add(PersistedUser(to_user_id(user), PersistReason.WHITE_LIST))

    def in_blacklist(self, user) -> bool:
        return to_user_id(user) in self._blacklist

    def in_whitelist(self, user) -> bool:
        return to_user_id(user) in self._whitelist

    def register_like(self, user) -> None:
        log.info(f"Registering like {user}")
        user_id = to_user_id(user)
        if user_id in self._interactions:
            inter = self._interactions[user_id]
        else:
            inter = UserInteraction(user_id)
        inter.likes_attempt += 1
        inter.last_like = datetime.now()
        self._interactions[user_id] = inter

    def get_liked(self, last_like=datetime.now(), likes_attempt=1) -> List[UserInteraction]:
        log.info(f"Collecting like info since {last_like} with like attempts {likes_attempt}")
        liked = []
        for interaction in self._interactions.values():
            if interaction.likes_attempt >= likes_attempt and \
                    interaction.last_like < last_like:
                liked.append(interaction)

        return liked

    def remove_interaction(self, user):
        log.info(f"Removing interaction {user}")
        del self._interactions[to_user_id(user)]

    def store_data(self):
        log.info(f"Flushing data")
        self._store_to_storage("interactions", self._interactions)
        self._store_to_storage("white_list", self._whitelist)
        self._store_to_storage("black_list", self._blacklist)
