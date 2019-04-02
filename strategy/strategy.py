from abc import ABC
from typing import List, Callable

from data_provider import Media, Engine, User


class MediaSource(ABC):

    def __init__(self, data_provider: Engine = None):
        self._data_provider = data_provider

    def init(self, data_provider: Engine) -> None:
        self._data_provider = data_provider

    def get_media(self, pages: int = 1) -> List[Media]:
        raise NotImplementedError()

    def __repr__(self) -> str:
        return f"MediaSource(" \
               f"data_provider={self._data_provider}, " \
               f")"


class Strategy(ABC):

    def __init__(self, data_provider: Engine = None,
                 call_delay=1.0, debug=False) -> None:
        self._data_provider = data_provider
        self._media_filter = None
        self._user_filter = None
        self._call_delay = call_delay
        self._error_delay = 2 * 60
        if data_provider is not None:
            self._own_id = data_provider.get_own_id()
        else:
            self._own_id = -1
        self._debug = debug

    def init(self, data_provider: Engine) -> None:
        self._data_provider = data_provider
        self._own_id = data_provider.get_own_id()

    def set_media_filter(self, media_filter: Callable[[Media], bool]):
        self._media_filter = media_filter

    def set_user_filter(self, user_filter: Callable[[User], bool]):
        self._user_filter = user_filter

    def __repr__(self) -> str:
        return f"Strategy(" \
               f"debug={self._debug}, " \
               f"own_id={self._own_id}, " \
               f"call_delay={self._call_delay}, " \
               f"data_provider={self._data_provider}, " \
               f"media_filters={self._media_filter}, " \
               f"user_filters={self._user_filter}" \
               f")"
