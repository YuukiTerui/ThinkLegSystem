import os
import csv
import time
import serial


class Arduino:
    def __init__(self, path='./', fname='arduino') -> None:
        self.path = path
        self.fname = fname
        self.data_cnt = 0
        self.datas = []
        self.start_time = None
        self.running = False
        
        self.port = 'COM6' if os.name == 'nt' else '/dev/ttyACM0'
        self.baudrate = 115200
        self.timeout = 0.5
        self.serial = serial.Serial(self.port, self.baudrate, timeout=self.timeout)#, dsrdtr=True)
        self.flush_buffer()
        
        print(self.serial)

    @property
    def data(self):
        return self.datas[-1]

    def __serve(self):
        data = self.serial.readline()
        try:
            data = data.decode('utf-8').replace('\n', '').split(',')
        except Exception as e:
            print(data)
            data = None
        return data

    def flush_buffer(self):
        self.serial.reset_output_buffer()
        self.serial.reset_input_buffer()

    def run(self):
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
        self.run()

    def stop(self):
        self.serial.write(b'0')
        self.running = False

    def reset(self):
        self.serial.write(b'9')
        self.running = False

    def close(self):
        self.serial.close()

    def save(self):
        with open(f'{self.path}{self.fname}.csv', 'w') as f:
            weiter = csv.writer(f)
            weiter.writerows(self.datas)


def main():
    ard = Arduino()
    ard.start()
    try:
        while True:
            data = ard.data
            print(data)
    except KeyboardInterrupt as e:
        print('finish with Cntl-C')
        ard.close()
    



if __name__ == '__main__':
    main()