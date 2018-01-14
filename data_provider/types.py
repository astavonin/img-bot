from abc import ABC, abstractmethod

from .tools import shorten_string


class User(ABC):
    @property
    @abstractmethod
    def id(self):
        raise NotImplemented()

    @property
    @abstractmethod
    def user_name(self):
        raise NotImplemented()

    @property
    @abstractmethod
    def full_name(self):
        raise NotImplemented()

    @property
    @abstractmethod
    def is_private(self):
        raise NotImplemented()

    @property
    @abstractmethod
    def is_business(self):
        raise NotImplemented()

    @property
    @abstractmethod
    def media_count(self):
        raise NotImplemented()

    @property
    @abstractmethod
    def follower_count(self):
        raise NotImplemented()

    @property
    @abstractmethod
    def following_count(self):
        raise NotImplemented()

    @property
    @abstractmethod
    def external_url(self):
        raise NotImplemented()

    @property
    @abstractmethod
    def profile_url(self):
        raise NotImplemented()

    @property
    @abstractmethod
    def has_chaining(self):
        raise NotImplemented()

    def __repr__(self) -> str:
        return "User(id={}, " \
               "user_name={}, " \
               "full_name={}, " \
               "is_private={}, " \
               "is_business={}, " \
               "media_count={}, " \
               "follower_count={}, " \
               "following_count={}, " \
               "external_url={}, " \
               "profile_url={}, " \
               "has_chaining={}" \
               ")".format(self.id, shorten_string(self.user_name),
                          shorten_string(self.full_name), self.is_private,
                          self.is_business, self.media_count,
                          self.follower_count, self.following_count,
                          self.external_url, self.profile_url, self.has_chaining
                          )


class Media(ABC):
    @property
    @abstractmethod
    def id(self):
        raise NotImplemented()

    @property
    @abstractmethod
    def like_count(self):
        raise NotImplemented()

    @property
    @abstractmethod
    def has_liked(self):
        raise NotImplemented()

    @property
    @abstractmethod
    def user(self):
        raise NotImplemented()

    @property
    @abstractmethod
    def user_tags(self):
        raise NotImplemented()

    @property
    @abstractmethod
    def comments_count(self):
        raise NotImplemented()

    @property
    @abstractmethod
    def image(self):
        raise NotImplemented()

    @property
    @abstractmethod
    def raw_caption(self):
        raise NotImplemented()

    @property
    @abstractmethod
    def tags(self):
        raise NotImplemented()

    @property
    @abstractmethod
    def location(self):
        raise NotImplemented()

    @property
    @abstractmethod
    def date(self):
        raise NotImplemented()

    def __repr__(self) -> str:
        return "Media(" \
               "id=\"{}\", " \
               "like_count={}, " \
               "has_liked={}, " \
               "user={}, " \
               "comments_count={}, " \
               "image={}, " \
               "raw_caption=\"{}\", " \
               "tags={}, " \
               "location={}, " \
               "date={}, " \
               "user_tags={}" \
               ")".format(self.id, self.like_count,
                          self.has_liked, self.user, self.comments_count,
                          self.image, shorten_string(self.raw_caption),
                          self.tags, self.location, self.date,
                          self.user_tags
                          )


class Location(ABC):
    @property
    @abstractmethod
    def id(self):
        raise NotImplemented()

    @property
    @abstractmethod
    def name(self):
        raise NotImplemented()

    @property
    @abstractmethod
    def address(self):
        raise NotImplemented()

    @property
    @abstractmethod
    def city(self):
        raise NotImplemented()

    @property
    @abstractmethod
    def latitude(self):
        raise NotImplemented()

    @property
    @abstractmethod
    def longitude(self):
        raise NotImplemented()

    def __repr__(self) -> str:
        return "Media(" \
               "id={}, " \
               "name={}, " \
               "address={}, " \
               "city={}, " \
               "latitude={}, " \
               "longitude={}" \
               ")".format(self.id, self.name, self.address, self.city,
                          self.latitude, self.longitude
                          )


class Comment(ABC):
    @property
    @abstractmethod
    def id(self):
        raise NotImplemented()

    @property
    @abstractmethod
    def user(self):
        raise NotImplemented()

    @property
    @abstractmethod
    def text(self):
        raise NotImplemented()

    @property
    @abstractmethod
    def created_at(self):
        raise NotImplemented()

    @property
    @abstractmethod
    def has_liked_comment(self):
        raise NotImplemented()

    def __repr__(self) -> str:
        return "Media(" \
               "id={}, " \
               "user={}, " \
               "text={}, " \
               "created_at={}, " \
               "has_liked_comment={}" \
               ")".format(self.id, self.user, shorten_string(self.text),
                          self.created_at, self.has_liked_comment
                          )
