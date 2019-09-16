import logging
import os
import traceback
from typing import List

from bot import Bot, MediaTask
from data_provider import User, get_engine, EngineType
from strategy import HashtagMediaSource, UserLiker


def is_in_string(data: str, words: List[str]):
    to_test = data.lower()
    for word in words:
        if to_test.find(word) is not -1:
            return True
    return False


def load_list(content: str) -> List[str]:
    return content.split(",")


def user_filter(user: User) -> bool:
    if user.media_count < 9:
        return False

    if user.following_count > 1000:
        return False

    if user.follower_count > 2000:
        return False

    if user.following_count > 0 and \
            user.follower_count / user.following_count > 20:
        return False

    return True


def process(uname: str, password: str, hashtags: str):
    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO,
                        datefmt='%Y/%m/%d %I:%M:%S')

    session = None
    session_file = "session.dat"
    try:
        with open(session_file, "r") as f:
            session = eval(f.read())
    except IOError:
        pass

    try:
        engine = get_engine(EngineType.INSTAGRAM)
        if not session:
            engine.login(uname, password)
            if os.environ.get('IMG_BOT_PERSIST'):
                with open(session_file, "w") as f:
                    f.write(str(engine.save()))
        else:
            engine.restore(session)

        bot = Bot(engine)

        media_like = MediaTask()
        media_source = HashtagMediaSource(load_list(hashtags))
        media_like.add_media_source(media_source)
        liker = UserLiker(total_likes=200, debug=False)
        liker.set_user_filter(user_filter)
        media_like.add_strategy(liker)
        bot.add_task(media_like)

        # stat_collect = CommonTask()
        # stat_collect.add_strategy(StatCollector("stat.txt"))
        # bot.add_task(stat_collect)

        bot.run()

    except RuntimeError as ex:
        print("Error: {}".format(ex))
        traceback.print_tb(ex.__traceback__)
