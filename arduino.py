# coding: utf-8
import os
import csv
import time
import serial
import threading
from json import load
from logging import config, getLogger
with open('./config/log_conf.json', 'r') as f:
    config.dictConfig(load(f))


class Arduino:
    def __init__(self, path='./', fname='ard_data') -> None:
        self.logger = getLogger(__name__)
        self.path = path
        self.fname = fname
        self.data_cnt = 0
        self.columns = ['msec', 'voltage']
        self.datas = [[0, 0]]
        self.start_time = None
        self.running = False
        self.thread = None
        
        self.port = 'COM6' if os.name == 'nt' else '/dev/ttyACM0'
        self.baudrate = 115200
        self.timeout = 0.5
        self.serial = serial.Serial(self.port, self.baudrate, timeout=self.timeout)#, dsrdtr=True)
        #self.flush_buffer()
        while True:
            tmp = self.serial.readlines()
            self.logger.debug(tmp)
            if tmp == [b'arduino is avairable\n']:
                break
        self.logger.info(self.serial)

    @property
    def data(self):
        return self.datas[-1]

    def __serve(self):
        self.logger.debug('in')
        data = self.serial.readline()
        try:
            data = list(map(int, data.decode('utf-8').replace('\n', '').split(',')))
        except Exception as e:
            self.logger.warning('%s %s', data, e)
            data = None
        return data

    def flush_buffer(self):
        self.logger.debug('in')
        self.serial.reset_output_buffer()
        self.serial.reset_input_buffer()

    def run(self):
        self.logger.debug('in')
        try:
            while self.running:
                data = self.__serve()
                if data:
                    self.datas.append(data)

        except:
            pass
        else:
            pass
        finally:
            pass

    def start(self):
        self.serial.write(b'1')
        self.running = True
        t, v = self.__serve()
        self.start_time = int(t)
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def stop(self):
        self.running = False
        self.serial.write(b'0')
        self.thread.join()
        
    def reset(self):
        self.running = False
        self.serial.write(b'9')

    def close(self):
        self.serial.close()

    def save(self):
        with open(f'{self.path}{self.fname}.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(self.columns)
            writer.writerows(self.datas)


def main():
    ard = Arduino()
    try:
        ard.start()
        while True:
            ard.logger.info(ard.data)
            time.sleep(0.02)
    except KeyboardInterrupt as e:
        print('finish with Cntl-C')
        ard.stop()
        ard.close()
        ard.save()
    



if __name__ == '__main__':
    main()