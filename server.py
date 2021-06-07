# coding: utf-8

from sys import winver
import time
import socket
import threading
import json
from logging import config, getLogger
with open('./config/log_conf.json', 'r') as f:
    config.dictConfig(json.load(f))


class ThinkLegServer:
    CLIENT_NUM = 10
    BUFFERSIZE = 2 ** 10
    def __init__(self, host='localhost', port=12345) -> None:
        self.logger = getLogger('thinkleg.server')
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_running = False

    def run(self):
        self.is_running = True
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen(self.CLIENT_NUM)
        while self.is_running:
            self.logger.info('Waiting for connection.')
            client_socket, address = self.socket.accept()
            client_socket.settimeout(5)
            self.logger.info('Established connection.')
            t = threading.Thread(target=self.connect_client, args=(client_socket, address))
            t.setDaemon(True)
            t.start()
            self.logger.info("thread %s started.", t)

    def connect_client(self, client, client_address):
        while True:
            try:
                msg = client.recv(self.BUFFERSIZE)
                self.logger.info('receive msg:%s from %s', msg, client_address)
                client.send(';')
                time.sleep(1)
            except socket.error as e:
                self.logger.warning('socket error:%s', e)
                client.close()
                break


def main():
    server = ThinkLegServer()
    server.run()

if __name__ == '__main__':
    main()