import RPi.GPIO as GPIO
import time
from datetime import datetime
import argparse
import csv

def readadc(adcnum, clockpin, mosipin, misopin, cspin):
    if adcnum > 7 or adcnum < 0:
        return -1

    GPIO.output(cspin, GPIO.HIGH)
    GPIO.output(clockpin, GPIO.LOW)
    GPIO.output(cspin, GPIO.LOW)

    commandout = adcnum
    commandout |= 0x18
    commandout <<= 3
    for i in range(5):
        if commandout & 0x80:
                GPIO.output(mosipin, GPIO.HIGH)
        else:
                 GPIO.output(mosipin, GPIO.LOW)
        commandout <<= 1
        GPIO.output(clockpin, GPIO.HIGH)
        GPIO.output(clockpin, GPIO.LOW)
    adcout = 0
    for i in range(11):
        GPIO.output(clockpin, GPIO.HIGH)
        GPIO.output(clockpin, GPIO.LOW)
        adcout <<= 1
        if i>0 and GPIO.input(misopin)==GPIO.HIGH:
            adcout |= 0x1
    GPIO.output(cspin, GPIO.HIGH)
    return adcout


def init_adc(SPICLK, SPIMOSI, SPIMISO, SPICS, READPIN):
    GPIO.setup(SPICLK, GPIO.OUT)
    GPIO.setup(SPIMOSI, GPIO.OUT)
    GPIO.setup(SPIMISO, GPIO.IN)
    GPIO.setup(SPICS, GPIO.OUT)
    GPIO.setup(READPIN, GPIO.OUT)
    GPIO.output(READPIN, GPIO.HIGH)


def main(args):
    GPIO.setmode(GPIO.BCM)
    SPICS = 8
    SPIMISO = 9
    SPIMOSI = 10
    SPICLK = 11
    READPIN = 25
    channel = 0
    init_adc(SPICLK, SPIMOSI, SPIMISO, SPICS, READPIN)

    fname = args.name
    run_time = args.time
    sleep_time = 1 / args.hz

    dir_ = r'./raw/'
    f = open(dir_+args.name+'.csv', 'a', newline='')
    writer = csv.writer(f)
    try:
        t_s = time.time()
        t = 0
        while t < run_time:
            t = time.time() - t_s
            value = readadc(channel, SPICLK, SPIMOSI, SPIMISO, SPICS)
            writer.writerow([t, value])
            print('time: {:.2f}/{}\t\tvalue: {}'.format(t, run_time, value))
            time.sleep(sleep_time)

    except KeyboardInterrupt as e:
        print(e)

    finally:
        print('finish.')
        f.close()
        GPIO.cleanup()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name',type=str, default=datetime.now().isoformat())
    parser.add_argument('-t', '--time', type=int, default=60)
    parser.add_argument('--hz', type=int, default=2)
    args = parser.parse_args()
    main(args)
