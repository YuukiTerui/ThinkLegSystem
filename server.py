# coding: utf-8

import time
import socket
import threading
from collections import deque
import json
from logging import config, exception, getLogger
with open('./config/log_conf.json', 'r') as f:
    config.dictConfig(json.load(f))


class ThinkLegServer(threading.Thread):
    CLIENT_NUM = 10
    BUFFERSIZE = 2 ** 10
    def __init__(self, host='localhost', port=12345) -> None:
        super(ThinkLegServer, self).__init__()
        self.daemon = True
        self.name = __name__
        self.event = threading.Event()
        self.logger = getLogger('thinkleg.server')

        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))

        self.is_running = False
        self.data_queue = deque()
        
    @property
    def data(self):
        try:
            data = self.data_queue.popleft()
            self.event.clear()
            self.logger.debug('data is poped.')
            return data
        except IndexError as e:
            self.logger.debug('server_queue is empty.')
            return None
    
    def clear_data(self):
        self.logger.info('data is cleard.')
        self.data_queue.clear()

    def run(self):
        self.is_running = True
        self.socket.listen(self.CLIENT_NUM)
        while self.is_running:
            self.logger.info('Waiting for connection.')
            try:
                client_socket, address = self.socket.accept()
                #client_socket.settimeout(5)
            except KeyboardInterrupt as e:
                self.is_running = False
                self.logger.debug('receiving cntl-C')
            except Exception as e:
                self.logger.error('%s', e)
            else:
                self.logger.info('Established connection.')
                t = threading.Thread(target=self.connect_client, args=(client_socket, address), daemon=True)
                t.start()
            self.logger.info("thread %s started.", t)
            time.sleep(1)
        self.logger.info('stop running')

    def connect_client(self, client, client_address):
        while True:
            try:
                msg = client.recv(self.BUFFERSIZE).decode('utf-8')
                self.logger.info('receive msg: %s from %s', msg, client_address)
                client.send(';'.encode('utf-8'))
                self.data_queue.append(msg)
                self.event.set()
            except socket.error as e:
                self.logger.warning('socket error:%s', e)
                client.close()
                break


def main():
    server = ThinkLegServer()
    server.start()

    time.sleep(1)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client.connect(('localhost', 12345))

    while True:
        msg = input('>')
        client.send(msg.encode('utf-8'))

if __name__ == '__main__':
    main()