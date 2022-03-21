#!/usr/bin/python3
import datetime
import json

from action.runer import RunMan
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

    runmen = []
    timestamp = get_timestamp()
    checker = OkxProInfoChecker(api_key, secret_key, phrase, timestamp, {'instType': 'SPOT'})
    ok_runman = RunMan(checker)
    runmen.append(ok_runman)
    looper = Looper(5, runmen)

    looper.loop()


if __name__ == '__main__':
    main()
