import logging
from time import sleep
from typing import List

from data_provider import Media, Engine, User
from data_provider import TooManyRequests
from strategy import Strategy

log = logging.getLogger(__name__)


class UserLiker(Strategy):

    def __repr__(self) -> str:
        return "UserLiker({}, " \
               "likes_per_user={}" \
               ")".format(super().__repr__(),
                          self._likes_per_user)

    def __init__(self, likes_per_user=5, total_likes=100, data_provider: Engine = None,
                  call_delay=0.5, debug=False) -> None:
        super().__init__(data_provider, call_delay, debug)
        self._likes_per_user = likes_per_user
        self._total_likes = total_likes

    def _like_user(self, user: User):
        log.info(f"{self._own_name} will add {self._likes_per_user} likes to {user}")
        if self._debug:
            print("===============FAKE LIKE============")
            print(f"BIO:\t{user.biography}")
            print(f"Name:\t{user.user_name}")
            print(f"Cat:\t{user.category}")
            print("====================================")
            return

        user_media = self._data_provider.get_user_feed(user)
        for i in range(self._likes_per_user):
            log.debug(f"Sleeping for {self._call_delay} for {self._own_name}")
            sleep(self._call_delay)
            self._data_provider.add_like(user_media[i])

    def process_media(self, medias: List[Media]) -> None:
        users = set()
        for m in medias:
            if m.user.id != self._own_id:  # we do not want to like ourselves
                users.add(m.user)
        users_to_like = int(self._total_likes / self._likes_per_user)
        log.info(f"{self._total_likes} likes was requested for {self._own_name}, "
                 f"going to like {users_to_like} users")
        error_delay = self._error_delay
        for user in users:
            try:
                log.debug(f"Sleeping for {self._call_delay} for {self._own_name}")
                sleep(self._call_delay)

                if users_to_like <= 0:
                    break

                full_user = self._data_provider.get_user_info(user)

                if self._user_filter(full_user):
                    self._like_user(user)
                    users_to_like -= 1
            except TooManyRequests:
                log.warning(f"Too many requests for {self._own_name}, sleeping for {error_delay}s")
                sleep(error_delay)
                error_delay *= 2
                self._call_delay *= 2
        print("{} user was liked by {}".format(int(self._total_likes / self._likes_per_user) - users_to_like,
                                                  self._own_name))
