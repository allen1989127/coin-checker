# -*- coding=utf-8 -*-
import base64
import hmac
import requests
from abc import ABCMeta, abstractmethod


class OkxChecker:
    __metaclass__ = ABCMeta

    API_PATH = 'https://www.okx.com'

    def __init__(self, api_key, secret_key, phrase, timestamp):
        self.api_key = api_key
        self.secret_key = secret_key
        self.phrase = phrase
        self.timestamp = timestamp

    @abstractmethod
    def request(self, **kwargs):
        pass


class OkxProInfoChecker(OkxChecker):
    METHOD = 'GET'
    REQUEST_PATH = '/api/v5/market/tickers'

    def __init__(self, api_key, secret_key, phrase, timestamp):
        super().__init__(api_key, secret_key, phrase, timestamp)
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
            'OK-ACCESS-SIGN': self.__signature(self.timestamp, method, request_path, body,
                                               self.secret_key),
            'OK-ACCESS-TIMESTAMP': self.timestamp,
            'OK-ACCESS-PASSPHRASE': self.pass_phrase,
        }

    def request(self, **kwargs):
        body = '{'
        params = {}
        for key, value in kwargs.items():
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
        return requests.get(url=self.url, params=params, headers=headers).json()
