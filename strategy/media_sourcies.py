import logging
from typing import List

import math

from data_provider import Media, Engine
from strategy import MediaSource

log = logging.getLogger(__name__)


class HashtagMediaSource(MediaSource):

    def __init__(self, hashtag: str, data_provider: Engine = None):
        super().__init__(data_provider)
        self._hashtag = hashtag

    def get_media(self, pages: int) -> List[Media]:
        return self._data_provider.get_hashtag_feed(self._hashtag, pages)

    def __repr__(self) -> str:
        return "HashtagMediaSource(" \
               "{hashtag={}}" \
               ")".format(self._hashtag, super().__repr__())


class TimelineMediaSource(MediaSource):

    def get_media(self, pages: int) -> List[Media]:
        return self._data_provider.get_timeline_feed(pages)

    def __repr__(self) -> str:
        return "TimelineMediaSource(" \
               "{}" \
               ")".format(super().__repr__())
