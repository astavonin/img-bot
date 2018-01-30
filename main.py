import logging
import traceback
from datetime import timedelta
from getpass import getpass
from typing import List

from bot import Task, Bot
from data_provider import get_engine, EngineType, User
from persistence import UsersStorage, PersistReason
from strategy.media_sourcies import HashtagMediaSource
from strategy.user_strategies import UserLiker


def is_in_string(data: str, words: List[str]):
    to_test = data.lower()
    for word in words:
        if to_test.find(word) is not -1:
            return True
    return False


def user_filter(user: User, us: UsersStorage) -> bool:
    white_list = ["model", "actor", "modelling", "photomodel"]

    black_list = ["store", "shop", "discounts", "free", "dealership", "brand"]

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
        us = UsersStorage("bw_lists.dat")

        bot = Bot(engine, us)

        task = Task()
        media_source = HashtagMediaSource(["model", "portrait"], engine)
        task.add_media_source(media_source)
        liker = UserLiker(debug=True)
        liker.set_user_filter(user_filter)
        task.add_strategy(liker)

        bot.add_task(task, timedelta(hours=4))

        bot.run()

    except RuntimeError as ex:
        print("Error: {}".format(ex))
        traceback.print_tb(ex.__traceback__)


if __name__ == '__main__':
    main()
