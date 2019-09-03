import json
import logging
import os
import traceback
from typing import List

from bot import MediaTask, Bot
from data_provider import get_engine, EngineType, User
from strategy import HashtagMediaSource, UserLiker


def is_in_string(data: str, words: List[str]):
    to_test = data.lower()
    for word in words:
        if to_test.find(word) is not -1:
            return True
    return False


def load_list(env_name) -> List[str]:
    content = os.environ.get(env_name)
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


def process():
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
            uname = os.environ.get('IMG_BOT_USER_NAME')
            password = os.environ.get('IMG_BOT_PASSWORD')
            engine.login(uname, password)
            if os.environ.get('IMG_BOT_PERSIST'):
                with open(session_file, "w") as f:
                    f.write(str(engine.save()))
        else:
            engine.restore(session)

        bot = Bot(engine)

        media_like = MediaTask()
        hashtags = load_list("IMG_BOT_HASHTAGS")
        media_source = HashtagMediaSource(hashtags)
        media_like.add_media_source(media_source)
        liker = UserLiker(total_likes=10, debug=True)
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


def response(status=200, headers=None, body=''):
    if not body:
        return {'statusCode': status}

    if headers is None:
        headers = {'Content-Type': 'application/json'}

    return {
        'statusCode': status,
        'headers': headers,
        'body': json.dumps(body)
    }


def lambda_handler(event, context):
    process()
    return response(status=200, body=event['body'])


def main():
    process()


if __name__ == '__main__':
    main()
