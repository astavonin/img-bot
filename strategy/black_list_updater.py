import logging
from datetime import datetime, timedelta

from data_provider import Engine
from persistence import UsersStorage, PersistReason
from strategy import Strategy

log = logging.getLogger(__name__)


class BlackListUpdater(Strategy):

    def __repr__(self) -> str:
        return "BlackListUpdater({})".format(super().__repr__())

    def __init__(self, data_provider: Engine = None, persistence: UsersStorage = None, call_delay=1.0,
                 debug=False) -> None:
        super().__init__(data_provider, persistence, call_delay, debug)

        self._followers = []

    def process(self):
        before = set(self._followers)
        self._followers = self._data_provider.get_user_followers(pages=100)
        current = set(self._followers)
        bots = list(before - current)
        for bot in bots:
            self._persistence.add_to_blacklist(bot, PersistReason.BOT)

        liked = self._persistence.get_liked(datetime.now() - timedelta(days=2))
        follower_ids = set([follower.id for follower in current])
        blacklisted_count = len(bots)
        for like in liked:
            if like.user_id not in follower_ids:
                self._persistence.add_to_blacklist(like.user_id, PersistReason.NOT_FOLLOWED)
                self._persistence.remove_interaction(like.user_id)
                blacklisted_count += 1

        self._persistence.store_data()
        log.info(f"{blacklisted_count} users were blacklisted")
