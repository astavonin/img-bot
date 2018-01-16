from abc import ABC
from typing import Dict, List

from . import types


class Engine(ABC):
    # Session manipulations
    def restore(self, session: Dict[str, str]) -> None:
        raise NotImplementedError()

    def save(self) -> Dict[str, str]:
        raise NotImplementedError()

    def login(self, username, password) -> None:
        raise NotImplementedError()

    def logout(self) -> None:
        raise NotImplementedError()

    # Comments and likes
    def add_comment(self, media, text) -> types.Comment:
        raise NotImplementedError()

    def add_like(self, media) -> None:
        raise NotImplementedError()

    def delete_comment(self, media, comment) -> None:
        raise NotImplementedError()

    def delete_like(self, media) -> None:
        raise NotImplementedError()

    def follow(self, user) -> None:
        raise NotImplementedError()

    def unfollow(self, user) -> None:
        raise NotImplementedError()

    # Feeds manipulations
    def get_hashtag_feed(self, hashtag, pages=1) -> List[types.Media]:
        raise NotImplementedError()

    def get_timeline_feed(self, pages=1) -> List[types.Media]:
        raise NotImplementedError()

    def get_user_feed(self, user=None, pages=1, min_timestamp=None) -> List[types.Media]:
        raise NotImplementedError()

    # Media info
    def get_media(self, media) -> List[types.Media]:
        raise NotImplementedError()

    def get_media_comments(self, media, pages=1) -> List[types.Comment]:
        raise NotImplementedError()

    def get_media_likers(self, media) -> List[types.User]:
        raise NotImplementedError()

    def upload_media(self, img_path, caption, first_comment=None) -> types.Media:
        raise NotImplementedError()

    # User info
    def get_user_followers(self, user=None, pages=1) -> List[types.User]:
        raise NotImplementedError()

    def get_user_followings(self, user=None, pages=1) -> List[types.User]:
        raise NotImplementedError()

    def get_user_info(self, user=None) -> types.User:
        raise NotImplementedError()
