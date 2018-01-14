import logging
from getpass import getpass

from data_provider.instagram import API


def main():
    logging.basicConfig(level=logging.DEBUG)

    session = None
    session_file = "session.dat"
    try:
        with open(session_file, "r") as f:
            session = eval(f.read())
    except FileNotFoundError:
        pass

    try:
        api = API()
        if not session:
            uname = input("user name: ")
            password = getpass("password: ")
            api.login(uname, password)
        else:
            api.restore(session)

        # feed = api.get_timeline_feed()
        # print(api.add_like(feed[0]))
        # print(feed)
        # feed = api.get_hashtag_feed("model", 2)
        # print("len={}, {}".format(len(feed), feed))
        # uinfo = api.get_user_info(227793768)

        # print(api.add_comment(1664462516250872860, "test"))
        # print(api.delete_comment(1664462516250872860, 17891955247144228))

        # print(api.add_like(17891955247144228))
        feed = api.get_user_feed()
        print(f"Own feed: {feed}")
        for media in feed:
            if media.comments_count and media.comments_count > 0:
                comments = api.get_media_comments(media, 2)
                print(f"Comments on {media.id} {comments}")
            for tagged in media.user_tags:
                uinfo = api.get_user_info(tagged)
                print(f"tagged user {uinfo}")
                feed = api.get_user_feed(tagged, 2)
                print(f"tagged user feed {feed}")
        # print("len={}, {}".format(len(feed), feed))
        # uinfo = api.get_user_info()
        # print(uinfo)
        # followers = api.get_user_followers(pages=2)
        # print(followers)

        # likers = api.get_media_likers()

        with open(session_file, "w") as f:
            f.write(str(api.save()))

    except RuntimeError as ex:
        print("Error: {}".format(ex))


if __name__ == '__main__':
    main()
