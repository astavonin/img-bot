import logging
import re
from datetime import datetime

from data_provider.types import Media, User, Location, Comment
from data_provider.tools import get_or
from .config import USER_URL

log = logging.getLogger(__name__)


def extract_tags(text) -> [str]:
    return re.findall(r"#\w+", text)


class InstagramMedia(Media):
    def __init__(self, raw_data) -> None:
        super().__init__()
        try:
            self._id = raw_data["pk"]
            self._like_count = raw_data["like_count"]
            self._has_liked = raw_data["has_liked"]
            self._comments_count = get_or(raw_data, "comment_count", 0)
            if raw_data["caption"]:
                self._caption = raw_data["caption"]["text"]
            else:
                self._caption = ""
            self._user = InstagramUser(raw_data["user"])
            self._date = datetime.fromtimestamp(raw_data["taken_at"])
            if "usertags" in raw_data:
                users = raw_data["usertags"]["in"]
                self._user_tags = \
                    [InstagramUser(user["user"]) for user in users]
            else:
                self._user_tags = []
            if "location" in raw_data:
                self._location = InstagramLocation(raw_data["location"])
            else:
                self._location = None
            self._tags = extract_tags(self._caption)

        except Exception as ex:
            log.warning("Unable to parse InstagramMedia: {}. Data: {}"
                        .format(ex, raw_data))

    @property
    def user_tags(self):
        return self._user_tags

    @property
    def date(self):
        return self._date

    @property
    def id(self):
        return self._id

    @property
    def like_count(self):
        return self._like_count

    @property
    def has_liked(self):
        return self._has_liked

    @property
    def user(self):
        return self._user

    @property
    def comments_count(self):
        return self._comments_count

    @property
    def image(self):
        # TODO: implement `Image` first
        return None

    @property
    def raw_caption(self):
        return self._caption

    @property
    def tags(self):
        return self._tags

    @property
    def location(self):
        return self._location


class InstagramUser(User):
    def __init__(self, raw_data) -> None:
        super().__init__()
        try:
            self._id = raw_data["pk"]
            self._user_name = raw_data["username"]
            self._full_name = get_or(raw_data, "full_name", "")
            self._is_private = get_or(raw_data, "is_private", False)
            self._is_business = get_or(raw_data, "is_business", False)
            self._media_count = get_or(raw_data, "media_count", 0)
            self._follower_count = get_or(raw_data, "follower_count", 0)
            self._following_count = get_or(raw_data, "following_count", 0)
            self._external_url = get_or(raw_data, "external_url", "")
            self._profile_url = "{}/{}".format(USER_URL, self._user_name)
            self._has_chaining = get_or(raw_data, "has_chaining", False)
        except Exception as ex:
            log.warning("Unable to parse InstagramUser: {}. Data: {}"
                        .format(ex, raw_data))

    @property
    def has_chaining(self):
        return self._has_chaining

    @property
    def id(self):
        return self._id

    @property
    def user_name(self):
        return self._user_name

    @property
    def full_name(self):
        return self._full_name

    @property
    def is_private(self):
        return self._is_private

    @property
    def is_business(self):
        return self._is_business

    @property
    def media_count(self):
        return self._media_count

    @property
    def follower_count(self):
        return self._follower_count

    @property
    def following_count(self):
        return self._following_count

    @property
    def external_url(self):
        return self._external_url

    @property
    def profile_url(self):
        return self._profile_url


class InstagramLocation(Location):
    def __init__(self, raw_data) -> None:
        super().__init__()
        try:
            self._id = raw_data["pk"]
            self._name = raw_data["name"]
            self._address = raw_data["address"]
            self._city = raw_data["city"]
            self._latitude = raw_data["lat"]
            self._longitude = raw_data["lng"]
        except Exception as ex:
            log.warning("Unable to parse InstagramLocation: {}. Data: {}"
                        .format(ex, raw_data))

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def address(self):
        return self._address

    @property
    def city(self):
        return self._city

    @property
    def latitude(self):
        return self._latitude

    @property
    def longitude(self):
        return self._longitude


class InstagramComment(Comment):
    def __init__(self, raw_data) -> None:
        super().__init__()
        try:
            self._id = raw_data["pk"]
            self._user = InstagramUser(raw_data["user"])
            self._text = raw_data["text"]
            self._created_at = datetime.fromtimestamp(raw_data["created_at"])
            self._has_liked_comment = get_or(raw_data, "has_liked_comment", False)
        except Exception as ex:
            log.warning("Unable to parse InstagramComment: {}. Data: {}"
                        .format(ex, raw_data))

    @property
    def id(self):
        return self._id

    @property
    def user(self):
        return self._user

    @property
    def text(self):
        return self._text

    @property
    def created_at(self):
        return self._created_at

    @property
    def has_liked_comment(self):
        return self._has_liked_comment
