#!/usr/bin/python3
import datetime
import json
import constants

from check.checker import OkxProInfoChecker


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
    checker = OkxProInfoChecker(api_key, secret_key, phrase, timestamp)
    data = checker.request(instType='SPOT')
    print(data)


if __name__ == '__main__':
    main()
