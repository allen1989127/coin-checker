#!/usr/bin/python3
import datetime
import json

from common import constants

from action.checker import OkxProInfoChecker
from common.loop import Looper


def parse_config():
    with open('config.json', 'r') as f:
        return json.load(f)


def get_timestamp():
    now = datetime.datetime.now()
    t = now.isoformat('T', 'milliseconds')
    return t + 'Z'


def main():
    params = parse_config()
    api_key = params[constants.TAG_API_KEY]
    secret_key = params[constants.TAG_SECRET_KEY]
    phrase = params[constants.TAG_PHRASE]

    timestamp = get_timestamp()
    check_params = {'instId': 'ETH-USTD'}
    checker = OkxProInfoChecker(api_key, secret_key, phrase, timestamp, check_params)
    looper = Looper(5, checker)

    looper.loop()


if __name__ == '__main__':
    main()
