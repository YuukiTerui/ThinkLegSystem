# coding: utf-8
import os
import csv
import time
import serial
import socket
import threading
from collections import deque
from json import load
from logging import config, getLogger
with open('./config/log_conf.json', 'r') as f:
    config.dictConfig(load(f))

from mysocket.server import ThinkLegServer


class Arduino:
    def __init__(self, path='./data/arduino/', fname='ard_data') -> None:
        self.logger = getLogger('arduino')
        self.datalogger = getLogger('arduino.data')

        self.path = path
        self.fname = fname

        self.thinkleg_status = 0
        self.thinkleg_statuses = [0]
        
        self.columns = ['msec', 'voltage']
        self.raw = [[0, 0]]
        self.start_time = None
        self.is_running = False
        self.thread = None
        
        self.server = ThinkLegServer(host='localhost', port=10001)
        self.server.start()
        self.thread_observe_server = threading.Thread(target=self.server_process, daemon=True)
        self.thread_observe_server.start()
        
        self.port = 'COM6' if os.name == 'nt' else '/dev/ttyACM0'
        self.baudrate = 115200
        self.timeout = 0.5
        self.serial = serial.Serial(self.port, self.baudrate, timeout=self.timeout)#, dsrdtr=True)
        #self.flush_buffer()
        while True:
            msg = self.serial.readlines()
            self.logger.info(msg)
            if msg == [b'arduino is avairable\n']:
                break
        self.logger.info(self.serial)

    @property
    def data(self):
        return self.raw[-1]

    def __reserve(self):
        self.logger.debug('')
        data = self.serial.readline()
        try:
            data = list(map(int, data.decode('utf-8').replace('\n', '').split(',')))
            self.logger.debug('receive data: %s', data)
        except Exception as e:
            self.logger.warning('receiving data is failed.: %s %s', data, e)
            data = None
        return data

    def flush_buffer(self):
        self.logger.debug('')
        self.serial.reset_output_buffer()
        self.serial.reset_input_buffer()
        
    def server_process(self):
        while self.server:
            self.logger.debug('wait server event')
            self.server.event.wait()
            self.logger.debug('occur server event')
            msg = self.server.data
            if not msg:
                continue
            if msg == '1':
                self.logger.debug('reserve order to start.')
                self.start()
            elif msg == '0':
                self.logger.debug('reserve order to stop.')
                self.stop()
            elif msg == 'reset':
                self.logger.debug('reserve order to reset.')
                self.reset()
            elif msg == 'd':
                self.logger.info('%s', self.data)
            else:
                self.logger.warning('receive msg: %s', msg)
            
    def run(self):
        try:
            while self.is_running:
                data = self.__reserve()
                if len(data) == 2:
                    self.datalogger.debug('%s', data)
                    self.raw.append(data)
                    self.thinkleg_statuses.append(self.thinkleg_status)
        except:
            pass

    def start(self):
        self.logger.info('start arduino')
        self.serial.write(b'1')
        self.is_running = True
        t, v = self.__reserve()
        self.start_time = int(t)
        self.thread = threading.Thread(target=self.run, daemon=True)
        self.thread.start()

    def stop(self):
        self.is_running = False
        self.serial.write(b'0')
        self.thread.join()
        self.logger.info('stop arduino')
        
    def reset(self):
        self.is_running = False
        self.serial.write(b'9')
        self.flush_buffer()
        self.logger.info('reset arduino')

    def close(self):
        self.serial.close()

    def save(self, data=None):
        with open(f'{self.path}{self.fname}.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            if data == None:
                writer.writerow(self.columns)
                writer.writerows(self.raw)
                self.logger.info('save arduino raw data.')
            else:
                writer.writerow([*self.columns, 'status'])
                writer.writerows([[r, s] for r, s in zip(self.raw, self.thinkleg_statuses)])

class Controller:
    def __init__(self, host='localhost', port=10001) -> None:
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def connect(self):
        try:
            self.socket.connect((self.host, self.port))
            #self.logger.info('connected %s', self.host)
            return True
        except socket.error as e:
            #self.logger.warning('failed to connect %s', self.host)
            return False
    
    def send(self, data):
        if not isinstance(data, str):
            data = str(data)
        try:
            self.socket.send(data.encode('utf-8'))
        except socket.error as e:
            print(e)

def main():
    ard = Arduino()
    try:
        ard.start()
        while True:
            if ard.is_running:
                ard.logger.info(ard.data)
            time.sleep(0.02)
    except KeyboardInterrupt as e:
        ard.logger.info('finish with Cntl-C')
        ard.stop()
        ard.close()
        ard.save()
    



if __name__ == '__main__':
    main()