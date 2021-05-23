import os
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
        
    def init_serial(self):
        ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout, dsrdtr=True)
        ser.reset_output_buffer()
        ser.reset_input_buffer()
        return ser

    def get_data(self):
        data = self.serial.readline()
        print(data)
        return data


def main():
    arduino = Arduino()

    for _ in range(10):
        arduino.get_data()
        



if __name__ == '__main__':
    main()