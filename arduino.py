import os
import time
import serial


class Arduino:
    def __init__(self, fname='arduino', path='./') -> None:
        self.datas = None
        self.data = None
        self.start_time = None
        self.data_cnt = 0

        self.port = 'COM6' if os.name == 'nt' else '/dev/ttyACM0'
        self.baudrate = 9600
        self.timeout = 0.5
        self.serial = self.init_serial()

        self.fname = fname
        self.path = path

        print(self.serial)
        self.serial.write(b'0')
        
    def init_serial(self):
        ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout, dsrdtr=True)
        ser.reset_output_buffer()
        ser.reset_input_buffer()
        return ser

    def get_data(self):
        self.serial.write(b'd')
        data = self.serial.readline()
        return data


def main():
    arduino = Arduino()

    while True:
        data = arduino.get_data()
        print(data.decode('utf-8'))
        time.sleep(1)




if __name__ == '__main__':
    main()