# -*-coding:utf-8-*-
import smtplib
import logging

from common import constants, config
from email.mime.text import MIMEText
from email.header import Header

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class MailSender:
    def __init__(self, data: list, price: float, to_addr: str):
        self.data = data
        self.price = price
        self.to_addr = to_addr

    def __send(self, last_price):
        params = config.read_config()
        server = params[config.TAG_SMTP_SERVER]
        server = smtplib.SMTP(server)
        server.ehlo()
        server.starttls()
        from_addr = params[config.TAG_FROM_ADDR]
        password = params[config.TAG_PASSWORD]
        server.login(from_addr, password)

        msg_str = 'Hi there\nThe price of ' + self.data[constants.TAG_INST_ID] + ' is '
        if last_price > self.price:
            msg_str += 'above '
            code = 1
        elif last_price < self.price:
            msg_str += 'below '
            code = -1
        else:
            msg_str += 'equal '
            code = 0
        msg_str += str(self.price)
        msg_str += '\n'

        msg_str += 'The price now is ' + str(last_price)
        msg = MIMEText(msg_str, 'plain', 'utf-8')
        msg['Subject'] = Header('Coin tracker notify...', 'utf-8').encode()
        server.sendmail(from_addr, [self.to_addr], msg.as_string())
        logger.info('%s start sending email...' % from_addr)
        return code

    def do(self, check):
        last_price = float(self.data[constants.TAG_LAST_PRICE])
        if check > 0 and last_price > self.price:
            return 1
        if check < 0 and last_price < self.price:
            return -1

        return self.__send(last_price)
