import logging
import random
from typing import List, Set

from data_provider import Media, Engine
from strategy import MediaSource

log = logging.getLogger(__name__)


class HashtagMediaSource(MediaSource):

    def __init__(self, hashtags: List[str], random_tag=True, data_provider: Engine = None):
        super().__init__(data_provider)
        self._hashtags = hashtags
        self._random_tag = random_tag

    def get_media(self, pages: int = 1) -> List[Media]:
        medias = []
        if self._random_tag:
            hashtags = [random.choice(self._hashtags)]
        else:
            hashtags = self._hashtags
        for hashtag in hashtags:
            log.info(f"Loading medias for hashtag `{hashtag}`, {pages} page requested")
            medias.extend(self._data_provider.get_hashtag_feed(hashtag, pages))
        return medias

    def __repr__(self) -> str:
        return "HashtagMediaSource(" \
               "hashtags={}, " \
               "{})".format(self._hashtags, super().__repr__())


class TimelineMediaSource(MediaSource):

    def get_media(self, pages: int = 1) -> Set[Media]:
        return self._data_provider.get_timeline_feed(pages)

    def __repr__(self) -> str:
        return "TimelineMediaSource(" \
               "{}" \
               ")".format(super().__repr__())
