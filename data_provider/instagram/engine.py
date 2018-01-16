import requests
import json
import hashlib
import hmac
import urllib
import uuid
import logging
import urllib.parse

from requests.cookies import cookiejar_from_dict
from requests.utils import dict_from_cookiejar

from data_provider.types import Media, User, Comment
from data_provider.tools import get_or

from . import types, config

from data_provider import errors

log = logging.getLogger(__name__)


def generate_uuid(uuid_type):
    generated_uuid = str(uuid.uuid4())
    if uuid_type:
        return generated_uuid
    else:
        return generated_uuid.replace('-', '')


def generate_device_id(seed):
    volatile_seed = "12345"
    m = hashlib.md5()
    m.update(seed.encode('utf-8') + volatile_seed.encode('utf-8'))
    return 'android-' + m.hexdigest()[:16]


def generate_signature(data):
    parsed_data = urllib.parse.quote(data)
    return 'ig_sig_key_version=' + config.SIG_KEY_VERSION + '&signed_body=' + \
           hmac.new(config.IG_SIG_KEY.encode('utf-8'), data.encode('utf-8'),
                    hashlib.sha256).hexdigest() + '.' + parsed_data


def to_user_id(user):
    if isinstance(user, int):
        return user
    elif isinstance(user, User):
        user_id = user.id
    else:
        user_id = int(user)
    return user_id


def to_media_id(media):
    if isinstance(media, int):
        return media
    elif isinstance(media, Media):
        media_id = media.id
    else:
        media_id = int(media)
    return media_id


def to_comment_id(comment):
    if isinstance(comment, int):
        return comment
    elif isinstance(comment, Comment):
        comment_id = comment.id
    else:
        comment_id = int(comment)
    return comment_id


class Engine(object):
    def __init__(self):
        self._logged_in = False
        self._session = requests.Session()

        self._uuid = None
        self._phone_id = None
        self._device_id = None
        self._user_id = None
        self._rank_token = None
        self._token = None
        self._cookies = None

    def save(self):
        return {
            "device_id": self._device_id,
            "user_id": self._user_id,
            "rank_token": self._rank_token,
            "token": self._token,
            "uuid": self._uuid,
            "phone_id": self._phone_id,
            "cookies": self._cookies,
        }

    def restore(self, session):
        if not ("device_id" in session and "user_id" in session and
                "rank_token" in session and "token" in session and
                "uuid" in session and "phone_id" in session):
            raise RuntimeError("Cannot restore session")
        log.info("Restoring instagram session")

        self._device_id = session["device_id"]
        self._user_id = session["user_id"]
        self._rank_token = session["rank_token"]
        self._token = session["token"]
        self._uuid = session["uuid"]
        self._phone_id = session["phone_id"]
        self._cookies = session["cookies"]

        self._session.cookies = cookiejar_from_dict(self._cookies)
        self._logged_in = True

    def login(self, username, password):
        if self._logged_in:
            raise RuntimeWarning("Already login")
        if password is None or username is None:
            raise ValueError("username or/and password could not be empty")

        log.info("Instagram login requested for {}".format(username))

        m = hashlib.md5()
        m.update(username.encode('utf-8') + password.encode('utf-8'))
        self._device_id = generate_device_id(m.hexdigest())
        self._uuid = generate_uuid(True)
        self._phone_id = generate_uuid(True)

        url = 'si/fetch_headers/?challenge_type=signup&guid='
        url = url + generate_uuid(False)
        resp, _ = self._send_request(url, None)
        data = {'phone_id': self._phone_id,
                '_csrftoken': resp.cookies[
                    'csrftoken'],
                'username': username,
                'guid': self._uuid,
                'device_id': self._device_id,
                'password': password,
                'login_attempt_count': '0'}

        resp, data = self._send_request('accounts/login/', data)
        self._user_id = data["logged_in_user"]["pk"]
        self._rank_token = "%s_%s" % (self._user_id, self._uuid)
        self._token = resp.cookies["csrftoken"]
        self._cookies = dict_from_cookiejar(resp.cookies)
        self._logged_in = True
        log.info("Login successfully as {}!".format(username))

    def logout(self):
        if not self._logged_in:
            return
        log.info("Logout from instagram")
        self._logged_in = not self._send_request('accounts/logout/')

    def _send_request(self, endpoint, post=None):
        self._session.headers.update({'Connection': 'close',
                                      'Accept': '*/*',
                                      'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                                      'Cookie2': '$Version=1',
                                      'Accept-Language': 'en-US',
                                      'User-Agent': config.USER_AGENT})
        log.debug("Sending {} request to {}"
                  .format("POST" if post is not None else "GET", endpoint))
        if post is not None:  # POST
            data = {
                '_uuid': self._uuid,
                '_uid': self._user_id,
                '_csrftoken': self._token,
            }
            data.update(post)
            message = json.dumps(data)
            response = self._session.post(
                config.API_URL + endpoint, data=generate_signature(message))
        else:  # GET
            response = self._session.get(
                config.API_URL + endpoint)

        if response.status_code == 200:
            return response, json.loads(response.text)
        if response.status_code == 429:
            raise errors.TooManyRequests()
        elif response.status_code == 400:
            response_data = json.loads(response.text)
            raise errors.InternalHttpError(response_data.get('message'))
        else:
            raise errors.InternalHttpError("HTTP error {}".
                                           format(response.status_code))

    def get_timeline_feed(self, pages=1):
        log.info(f"get_timeline_feed pages={pages}")

        url = f'feed/timeline/?rank_token={self._rank_token}' \
              f'&ranked_content=true'

        items = self._load_items(url, pages, "items")

        return [types.InstagramMedia(item) for item in items]

    def upload_media(self, img_path, caption, first_comment=None):
        # TODO:
        raise NotImplemented()

    def get_media(self, media):
        media_id = to_media_id(media)

        log.info(f"get_media for media_id={media_id}")

        _, raw = self._send_request(f"media/{media_id}/info/")

        return [types.InstagramMedia(item) for item in raw["items"]]

    def add_comment(self, media, text):
        media_id = to_media_id(media)
        log.info(f"add_comment to media_id{media_id} with text '{text}'")

        _, raw = self._send_request(f"media/{media_id}/comment/",
                                    {'comment_text': text})

        return types.InstagramComment(raw["comment"])

    def delete_comment(self, media, comment):
        media_id = to_media_id(media)
        comment_id = to_comment_id(comment)
        log.info(f"delete_comment with media_id={media_id} and "
                 f"comment_id={comment_id}")

        self._send_request(f"media/{media_id}/comment/{comment_id}/delete/", {})

    def get_user_info(self, user=None):
        if user is None:
            user_id = self._user_id
        else:
            user_id = to_user_id(user)
        log.info(f"get_user_info for user_id={user_id}")

        _, raw = self._send_request(f'users/{user_id}/info/')

        return types.InstagramUser(raw["user"])

    def get_media_likers(self, media):
        media_id = to_media_id(media)
        log.info(f"get_media_likers for media_id={media_id}")

        likers = self._send_request('media/{media_id}/likers/?')
        return [types.InstagramUser(liker) for liker in likers]

    def _load_items(self, url, pages, data_root):
        maxid = ""
        items = []
        while pages > 0 and maxid is not None:
            _, feed = self._send_request(f'{url}&max_id={maxid}')
            maxid = get_or(feed, "next_max_id")
            items.extend(feed[data_root])
            pages -= 1
        return items

    def get_user_feed(self, user=None, pages=1, min_timestamp=None):
        if user is None:
            user_id = self._user_id
        else:
            user_id = to_user_id(user)
        log.info(
            f"get_user_feed for user_id=`{user_id}`, pages={pages}, "
            f"min_timestamp={min_timestamp}")

        url = f'feed/user/{user_id}/?min_timestamp={min_timestamp}&rank_token=' \
              f'{self._rank_token}&ranked_content=true'
        items = self._load_items(url, pages, "items")

        return [types.InstagramMedia(item) for item in items]

    def get_hashtag_feed(self, hashtag, pages=1):
        log.info(f"get_hashtag_feed for hashtag=`{hashtag}`, "
                 f"pages=`{pages}`")

        url = f'feed/tag/{hashtag}/?rank_token={self._rank_token}' \
              f'&ranked_content=true'
        items = self._load_items(url, pages, "items")

        return [types.InstagramMedia(item) for item in items]

    def get_user_followers(self, user=None, pages=1):
        if user is None:
            user_id = self._user_id
        else:
            user_id = to_user_id(user)
        log.info(f"get_user_followers for user_id={user_id}, pages={pages}")

        url = f"friendships/{user_id}/followers/?rank_token={self._rank_token}"
        medias = self._load_items(url, pages, "users")

        return [types.InstagramUser(media) for media in medias]

    def get_user_followings(self, user=None, pages=1):
        if user is None:
            user_id = self._user_id
        else:
            user_id = to_user_id(user)
        log.info(f"get_user_followings for user_id={user_id}, pages={pages}")

        url = f"friendships/{user_id}/following/?rank_token={self._rank_token}"
        medias = self._load_items(url, pages, "users")

        return [types.InstagramUser(media) for media in medias]

    def add_like(self, media):
        media_id = to_media_id(media)
        log.info(f"add_like for media_id={media_id}")

        self._send_request(f"media/{media_id}/like/",
                                  {'media_id': media_id})

    def delete_like(self, media):
        media_id = to_media_id(media)
        log.info(f"delete_like for media_id={media_id}")

        print(self._send_request(f"media/{media_id}/unlike/", {}))

    def get_media_comments(self, media, pages=1):
        media_id = to_media_id(media)
        log.info(f"get_media_comments for media_id={media_id}, pages={pages}")

        url = f"media/{media_id}/comments/?"
        comments = self._load_items(url, pages, "comments")

        return [types.InstagramComment(comment) for comment in comments]

    def follow(self, user):
        user_id = to_user_id(user)
        log.info("follow for user_id={user_id}")

        self._send_request(f"friendships/create/{user_id}/",
                                  {'user_id': user_id})

    def unfollow(self, user):
        user_id = to_user_id(user)
        log.info("unfollow for user_id={user_id}")

        self._send_request(f"friendships/destroy/{user_id}/",
                                  {'user_id': user_id})
