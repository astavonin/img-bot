import json
import os
import threading

from runner import process


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


def load_config() -> (str, str, str):
    with open("config.json", "r") as f:
        config = json.load(f)
        accounts = config.get("accounts", [])
        for account in accounts:
            yield account["uname"], account["password"], account["hashtags"]


def start_bot():
    jobs = []
    for args in load_config():
        job = threading.Thread(target=process, args=args)
        job.start()
        jobs.append(job)
    for job in jobs:
        job.join()


def lambda_handler(event, context):
    start_bot()
    return response(status=200, body=event.get('body', ''))


def main():
    start_bot()


if __name__ == '__main__':
    # NOTE: 403 on relogin request.
    main()
