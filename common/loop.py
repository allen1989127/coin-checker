# -*-coding=utf-8-*-
import time

from action.checker import OkxChecker


class Looper:
    def __init__(self, interval, checker: OkxChecker, sender):
        self.interval = interval
        self.checker = checker
        self.sender = sender

    def loop(self):
        while True:
            data = self.checker.request()
            print(data)

            time.sleep(self.interval)
