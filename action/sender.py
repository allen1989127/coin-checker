# -*-coding:utf-8-*-
import smtplib

from common import constants, config
from email.mime.text import MIMEText
from email.header import Header


class MailSender:
    def __init__(self, data: list, price: float, to_addr: str):
        self.data = data
        self.price = price
        self.to_addr = to_addr

    def __send(self, last_price):
        params = config.read_config()
        server = smtplib.SMTP(params[config.TAG_SMTP_SERVER], 25)
        from_addr = params[config.TAG_FROM_ADDR]
        server.login(from_addr, params[config.TAG_PASSWORD])

        msg_str = 'Hi there\nThe price of ' + self.data[constants.TAG_INST_ID] + ' is '
        if last_price > self.price:
            msg_str += ' above '
            code = 1
        elif last_price < self.price:
            msg_str += ' below '
            code = -1
        else:
            msg_str += ' equal '
            code = 0
        msg_str += str(self.price)
        msg_str += '\n'

        msg_str += 'The price now is ' + str(last_price)
        msg = MIMEText(msg_str, 'plain', 'utf-8')
        msg['Subject'] = Header('Coin tracker notify...', 'utf-8').encode()
        server.sendmail(from_addr, [self.to_addr], msg.as_string())
        return code

    def do(self, check):
        last_price = float(self.data[constants.TAG_LAST_PRICE])
        if check > 0 and last_price > self.price:
            return 1
        if check < 0 and last_price < self.price:
            return -1

        return self.__send(last_price)
