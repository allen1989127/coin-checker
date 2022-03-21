# -*-coding=utf-8-*-
import datetime
import time
import logging

from action.checker import OkxChecker, OkxProInfoChecker
from action.sender import MailSender
from common import constants, config


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def get_timestamp():
    now = datetime.datetime.now()
    t = now.isoformat('T', 'milliseconds')
    return t + 'Z'


class RunMan:
    def __init__(self, checker: OkxChecker, price: float, to_addr: str):
        self.checker = checker
        self.price = price
        self.to_addr = to_addr
        self.check = 0

    def run(self):
        data = self.checker.request()
        logger.info("checker request data")
        logger.info(str(data))
        if data is None or int(data['code']) != constants.CODE_SUCCESS:
            return

        sender = MailSender(data['data'][0], self.price, self.to_addr)
        next_check = sender.do(self.check)
        self.check = next_check


class Looper:
    def __init__(self, interval):
        self.interval = interval
        api_key = config.read_config()[config.TAG_API_KEY]
        secret_key = config.read_config()[config.TAG_SECRET_KEY]
        phrase = config.read_config()[config.TAG_PHRASE]
        pieces = config.read_config()[config.TAG_PIECES]
        self.runmen = []
        for piece in pieces:
            inst_id = piece[config.TAG_INST_ID]
            price = piece[config.TAG_PRICE]
            to_addr = piece[config.TAG_TO_ADDR]
            checker = OkxProInfoChecker(api_key, secret_key, phrase, {constants.TAG_INST_ID: inst_id})
            runman = RunMan(checker, price, to_addr)

            self.runmen.append(runman)

    def loop(self):
        while True:
            for runman in self.runmen:
                runman.run()

            time.sleep(self.interval)
