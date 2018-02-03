import logging
import traceback
from datetime import timedelta
from getpass import getpass
from typing import List

from bot import MediaTask, Bot, CommonTask
from data_provider import get_engine, EngineType, User
from persistence import UsersStorage, PersistReason
from strategy import HashtagMediaSource, UserLiker, StatCollector, BlackListUpdater


def is_in_string(data: str, words: List[str]):
    to_test = data.lower()
    for word in words:
        if to_test.find(word) is not -1:
            return True
    return False


def load_list(fname) -> List[str]:
    with open(fname) as f:
        content = f.readlines()
    return [x.strip() for x in content]


def user_filter(user: User, us: UsersStorage) -> bool:
    white_list = load_list("white_list.txt")
    black_list = load_list("black_list.txt")

    texts = user.biography + user.user_name + user.category

    if is_in_string(texts, black_list):
        us.add_to_blacklist(user, PersistReason.STOP_WORD)
        return False

    if is_in_string(texts, white_list):
        return True

    if user.media_count < 9:
        return False

    if user.following_count > 1000:
        us.add_to_blacklist(user, PersistReason.TOO_MANY_FOLLOWING)
        return False

    if user.follower_count > 2000:
        us.add_to_blacklist(user, PersistReason.TOO_MANY_FOLLOWERS)
        return False

    if user.following_count > 0 and \
            user.follower_count / user.following_count > 20:
        us.add_to_blacklist(user, PersistReason.BAD_FOLLOW_RATIO)
        return False

    return True


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
            with open(session_file, "w") as f:
                f.write(str(engine.save()))
        else:
            engine.restore(session)
        us = UsersStorage("db")

        bot = Bot(engine, us)

        media_like = MediaTask()
        hashtags = load_list("hashtags.txt")
        media_source = HashtagMediaSource(hashtags)
        media_like.add_media_source(media_source)
        liker = UserLiker(total_likes=150, debug=True)
        liker.set_user_filter(user_filter)
        media_like.add_strategy(liker)
        bot.add_task(media_like, timedelta(hours=4))

        stat_collect = CommonTask()
        stat_collect.add_strategy(StatCollector("stat.txt"))
        bot.add_task(stat_collect, timedelta(hours=1))

        stat_collect = CommonTask()
        stat_collect.add_strategy(BlackListUpdater())
        bot.add_task(stat_collect, timedelta(hours=3))

        bot.run()

    except RuntimeError as ex:
        print("Error: {}".format(ex))
        traceback.print_tb(ex.__traceback__)


if __name__ == '__main__':
    main()
