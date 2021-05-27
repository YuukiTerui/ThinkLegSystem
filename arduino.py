import os
import time
import serial


class Arduino:
    def __init__(self, fname='arduino', path='./') -> None:
        self.datas = None
        self.start_time = None
        self.data_cnt = 0
        self.fname = fname
        self.path = path
        
        self.port = 'COM6' if os.name == 'nt' else '/dev/ttyACM0'
        self.baudrate = 115200
        self.timeout = 0.5
        self.serial = serial.Serial(self.port, self.baudrate, timeout=self.timeout)#, dsrdtr=True)
        self.flush_buffer()
        
        print(self.serial)

    @property
    def data(self):
        data = self.serial.readline().decode('utf-8')
        return data
        
    def flush_buffer(self):
        self.serial.reset_output_buffer()
        self.serial.reset_input_buffer()

    def start(self):
        self.serial.write(b'1')

    def stop(self):
        self.serial.write(b'0')

    def reset(self):
        self.serial.write(b'9')
    


def main():
    arduino = Arduino()
    try:
        while True:
            data = arduino.get_data()
            try:
                print(data.decode('utf-8'))
            except Exception as e:
                print(e)
                print(data)
                return
            time.sleep(0.02)
    except KeyboardInterrupt as e:
        print('finish with Cntl-C')
        arduino.serial.close()





if __name__ == '__main__':
    main()