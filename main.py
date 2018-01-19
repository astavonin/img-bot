import logging
from getpass import getpass

from data_provider import get_engine, EngineType
from strategy.media_sourcies import HashtagMediaSource, TimelineMediaSource


def main():
    logging.basicConfig(level=logging.INFO)

    session = None
    session_file = "session.dat"
    try:
        with open(session_file, "r") as f:
            session = eval(f.read())
    except FileNotFoundError:
        pass

    try:
        engine = get_engine(EngineType.INSTAGRAM)
        if not session:
            uname = input("user name: ")
            password = getpass("password: ")
            engine.login(uname, password)
        else:
            engine.restore(session)

        # # media_source = HashtagMediaSource("model", engine)
        # media_source = TimelineMediaSource(engine)
        # medias = media_source.get_media(10)
        # for media in medias:
        #     print(media)

        # feed = engine.get_timeline_feed()
        # print(engine.add_like(feed[0]))
        # print(feed)
        # feed = engine.get_hashtag_feed("model", 2)
        # print("len={}, {}".format(len(feed), feed))
        # uinfo = engine.get_user_info(227793768)

        # print(engine.add_comment(1664462516250872860, "test"))
        # print(engine.delete_comment(1664462516250872860, 17891955247144228))

        # print(engine.add_like(17891955247144228))
        # feed = engine.get_user_feed()
        # print(f"Own feed: {feed}")
        # for media in feed:
        #     if media.comments_count and media.comments_count > 0:
        #         comments = engine.get_media_comments(media, 2)
        #         print(f"Comments on {media.id} {comments}")
        #     for tagged in media.user_tags:
        #         uinfo = engine.get_user_info(tagged)
        #         print(f"tagged user {uinfo}")
        #         feed = engine.get_user_feed(tagged, 2)
        #         print(f"tagged user feed {feed}")
        # print("len={}, {}".format(len(feed), feed))
        # uinfo = engine.get_user_info()
        # print(uinfo)
        # followers = engine.get_user_followers(pages=2)
        # print(followers)

        # likers = engine.get_media_likers()

        with open(session_file, "w") as f:
            f.write(str(engine.save()))

    except RuntimeError as ex:
        print("Error: {}".format(ex))


if __name__ == '__main__':
    main()
