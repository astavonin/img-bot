from datetime import datetime

from data_provider import Engine
from persistence import UsersStorage
from strategy import Strategy


class StatCollector(Strategy):

    def __init__(self, out_file: str, data_provider: Engine = None, persistence: UsersStorage = None,
                 call_delay=1.0, debug=False) -> None:
        super().__init__(data_provider, persistence, call_delay, debug)

        self._out_file = out_file

    def process(self):
        user = self._data_provider.get_user_info()
        with open(self._out_file, mode="a") as f:
            f.write("{:%Y-%m-%d %H:%M}\t{}\t{}\t{}\n".format(datetime.now(),
                                                             user.follower_count, user.following_count,
                                                             user.media_count))
