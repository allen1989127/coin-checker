# -*- coding=utf-8 -*-
import base64
import hmac

import requests
from abc import ABCMeta, abstractmethod

from common import loop


class OkxChecker:
    __metaclass__ = ABCMeta

    API_PATH = 'https://www.okx.com'

    def __init__(self, api_key, secret_key, phrase):
        self.api_key = api_key
        self.secret_key = secret_key
        self.phrase = phrase

    @abstractmethod
    def request(self) -> dict:
        pass


class OkxProInfoChecker(OkxChecker):
    METHOD = 'GET'
    REQUEST_PATH = '/api/v5/market/ticker'

    def __init__(self, api_key: str, secret_key: str, phrase: str, params: dict):
        super().__init__(api_key, secret_key, phrase)
        self.timestamp = ''
        self.params = params
        self.url = OkxChecker.API_PATH + OkxProInfoChecker.REQUEST_PATH

    def __signature(self, method, request_path, body):
        if str(body) == '{}' or str(body) == 'None':
            body = ''
        message = str(self.timestamp) + str.upper(method) + request_path + str(body)
        mac = hmac.new(bytes(self.secret_key, encoding='utf8'), bytes(message, encoding='utf-8'), digestmod='sha256')
        d = mac.digest()
        return base64.b64encode(d)

    def __get_header(self, method, request_path, body):
        return {
            'OK-ACCESS-KEY': self.api_key,
            'OK-ACCESS-SIGN': self.__signature(method, request_path, body),
            'OK-ACCESS-TIMESTAMP': self.timestamp,
            'OK-ACCESS-PASSPHRASE': self.phrase,
        }

    def request(self) -> dict:
        self.timestamp = loop.get_timestamp()

        body = '{'
        params = {}
        for key, value in self.params.items():
            body += '"'
            body += key
            body += '":"'
            body += value
            body += '",'

            params[key] = value
        if body.endswith(','):
            body = body[:-1]
        body += '}'
        headers = self.__get_header(OkxProInfoChecker.METHOD, OkxProInfoChecker.REQUEST_PATH, body)

        try:
            return requests.get(url=self.url, params=params, headers=headers).json()
        except requests.exceptions.HTTPError as e:
            return None
        except requests.exceptions.ConnectionError as e:
            return None
        except requests.exceptions.RequestException as e:
            return None
