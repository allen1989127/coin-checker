#!/usr/bin/python3
from common import constants, config
from common.loop import Looper


def main():
    looper = Looper(constants.INTERVAL)

    looper.loop()


if __name__ == '__main__':
    main()
