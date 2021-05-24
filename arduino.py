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
        while self.serial.read() != b'0':
            pass
        
    def init_serial(self):
        ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout)#, dsrdtr=True)
        ser.reset_output_buffer()
        ser.reset_input_buffer()
        return ser

    def get_data(self):
        data = self.serial.readline()
        return data


def main():
    arduino = Arduino()
    arduino.serial.write(b'0')

    try:
        while True:
            data = arduino.get_data()
            try:
                print(data.decode('utf-8'))
            except Exception as e:
                print(e)
                print(data)
            time.sleep(0.02)
    except KeyboardInterrupt as e:
        print('finish with Cntl-C')
        arduino.serial.close()





if __name__ == '__main__':
    main()