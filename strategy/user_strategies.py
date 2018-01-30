import logging
from time import sleep
from typing import List

from data_provider import Media, Engine, User
from data_provider.errors import TooManyRequests
from persistence import UsersStorage
from strategy import Strategy

log = logging.getLogger(__name__)


class UserLiker(Strategy):

    def __repr__(self) -> str:
        return "UserLiker({}, " \
               "likes_per_user={}" \
               ")".format(super().__repr__(),
                          self._likes_per_user)

    def __init__(self, likes_per_user=5, total_likes=100, data_provider: Engine = None,
                 persistence: UsersStorage = None, call_delay=1.0, debug=False) -> None:
        super().__init__(data_provider, persistence, call_delay, debug)
        self._likes_per_user = likes_per_user
        self._total_likes = total_likes

    def _like_user(self, user: User):
        log.info(f"Will add {self._likes_per_user} likes to {user}")
        if self._debug:
            print("===============FAKE LIKE============")
            print(f"BIO:\t{user.biography}")
            print(f"Name:\t{user.user_name}")
            print(f"Cat:\t{user.category}")
            print("====================================")
            return

        user_media = self._data_provider.get_user_feed(user)
        for i in range(self._likes_per_user):
            log.debug(f"Sleeping for {self._call_delay}")
            sleep(self._call_delay)
            self._data_provider.add_like(user_media[i])

    def process_media(self, medias: List[Media]) -> None:
        users = set()
        for m in medias:
            if m.user.id != self._own_id:  # we do not want to like ourselves
                users.add(m.user)
        users_to_like = int(self._total_likes / self._likes_per_user)
        log.info(f"{self._total_likes} likes was requested, going to like {users_to_like} users")
        error_delay = self._error_delay
        for user in users:
            try:
                log.debug(f"Sleeping for {self._call_delay}")
                sleep(self._call_delay)

                if users_to_like <= 0:
                    log.warning("All users was liked!")
                    break
                if self._persistence.in_blacklist(user):
                    log.info(f"User already is in black list: {user}")
                    continue
                if self._persistence.in_whitelist(user):
                    self._like_user(user)
                    users_to_like -= 1
                    continue

                full_user = self._data_provider.get_user_info(user)

                if self._user_filter(full_user, self._persistence):
                    self._like_user(user)
                    users_to_like -= 1
            except TooManyRequests:
                log.warning(f"Too many requests, sleeping for {error_delay}s")
                sleep(error_delay)
                error_delay *= 2
                self._call_delay *= 2
        log.info("{} user was liked".format(int(self._total_likes / self._likes_per_user) - users_to_like))
