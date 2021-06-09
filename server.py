# coding: utf-8

from sys import winver
import time
import socket
import threading
from collections import deque
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
        self.data_queue = deque()
        
    @property
    def data(self):
        try:
            data = self.data_queue.popleft()
            self.logger.debug('data is poped.')
            return data
        except IndexError as e:
            self.logger.debug('server_queue is empty.')
    
    def clear_data(self):
        self.logger.info('data is cleard.')
        self.data_queue.clear()

    def run(self):
        self.is_running = True
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
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
                t = threading.Thread(target=self.connect_client, args=(client_socket, address))
                t.setDaemon(True)
                t.start()
            self.logger.info("thread %s started.", t)
        self.logger.info('stop running')

    def connect_client(self, client, client_address):
        while True:
            try:
                msg = client.recv(self.BUFFERSIZE).decode('utf-8')
                self.logger.info('receive msg:%s from %s', msg, client_address)
                client.send(';'.encode('utf-8'))
                self.data_queue.append(msg)
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