
from os import error
from sys import winver
import time
import socket
import threading
import json
from logging import config, getLogger
with open('./config/log_conf.json', 'r') as f:
    config.dictConfig(json.load(f))


class ThinkLegClient:
    BUFFERSIZE = 2 ** 10
    EOF = ';'
    def __init__(self, host='localhost', port=12345) -> None:
        self.logger = getLogger('thinkleg.client')
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.is_running = False

    def create_connection(self):
        while True:
            try:
                self.socket.connect((self.host, self.port))
                self.logger.info('connected %s', self.host)
                return 
            except socket.error as e:
                self.logger.warning('failed to connect %s', self.host)
                time.sleep(1)
    
    def send_data(self, data):
        while True:
            try:
                self.socket.send(data.encode('utf-8'))
                msg = self.socket.recv(self.BUFFERSIZE).decode('utf-8')
                self.logger.info('msg: %s', msg)
                if msg == self.EOF:
                    self.logger.info('successful data transmission.: %s', data)
                    break
                else:

                    continue
            except socket.error as e:
                self.logger.warning('connection lost')
                self.create_connection(self.host, self.port)


def main():
    client = ThinkLegClient()
    client.create_connection()
    client.send_data('hello')


if __name__ == '__main__':
    main()