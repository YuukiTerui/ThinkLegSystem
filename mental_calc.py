# coding: utf-8

import os
import time
from mpyg321.mpyg321 import MPyg321Player


class MentalCalc:
    def __init__(self):
        self.sounds_path = './sounds/'
        self.sounds = sorted(os.listdir(self.sounds_path))
        self.player = MPyg321Player()

    def sound_test(self):
        for i in range(10):
            self.play(i)
            time.sleep(1)

    def play(self, i):
        print(f'play {self.sounds_path}{self.sounds[i]}')
        self.player.play_song(f'{self.sounds_path}{self.sounds[i]}')



def main():
    task = MentalCalc()
    task.sound_test()


if __name__ == '__main__':
    main()