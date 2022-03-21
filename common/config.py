# -*- coding:utf-8 -*-
import json

TAG_API_KEY = 'api_key'
TAG_SECRET_KEY = 'secret_key'
TAG_PHRASE = 'phrase'
TAG_SMTP_SERVER = 'smtp_server'
TAG_FROM_ADDR = 'from_addr'
TAG_PASSWORD = 'password'
TAG_PIECES = 'pieces'
TAG_INST_ID = 'inst_id'
TAG_PRICE = 'price'
TAG_TO_ADDR = 'to_addr'

__config = None


def read_config():
    if __config is None:
        return __parse_config()
    return __config


def __parse_config():
    with open('config.json', 'r') as f:
        return json.load(f)
