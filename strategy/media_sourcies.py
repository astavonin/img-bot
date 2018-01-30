import logging
from typing import List, Set

import math

from data_provider import Media, Engine
from strategy import MediaSource

log = logging.getLogger(__name__)


class HashtagMediaSource(MediaSource):

    def __init__(self, hashtags: List[str], data_provider: Engine = None):
        super().__init__(data_provider)
        self._hashtags = hashtags

    def get_media(self, pages: int = 1) -> List[Media]:
        medias = []
        for hashtag in self._hashtags:
            log.info(f"Loading medias for hashtag {hashtag}, {pages} page requested")
            medias.extend(self._data_provider.get_hashtag_feed(hashtag, pages))
        return medias

    def __repr__(self) -> str:
        return "HashtagMediaSource(" \
               "hashtags={}" \
               ")".format(self._hashtags, super().__repr__())


class TimelineMediaSource(MediaSource):

    def get_media(self, pages: int = 1) -> Set[Media]:
        return self._data_provider.get_timeline_feed(pages)

    def __repr__(self) -> str:
        return "TimelineMediaSource(" \
               "{}" \
               ")".format(super().__repr__())
