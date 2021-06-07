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
    def __init__(self, host, port) -> None:
        self.logger = getLogger('thinkleg.server')
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_running = False

    def run(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen(self.CLIENT_NUM)
        while self.is_running:
            self.logger.info("")
            client_socket, address = self.socket.accept()
