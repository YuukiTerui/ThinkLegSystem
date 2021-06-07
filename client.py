
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
    def __init__(self, host='localhost', port=12345) -> None:
        self.logger = getLogger('thinkleg.client')
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_running = False