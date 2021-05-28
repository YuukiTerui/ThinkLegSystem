# coding: utf-8

import os
from mpyg321.mpyg321 import MPyg321Player


class MentalCalc:
    def __init__(self):
        self.sounds_path = './sounds/'
        self.sounds = sorted(os.listdir(self.sounds_path))
        self.player = MPyg321Player()

    def test(self):
        for i in range(10):
            self.play(i)

    def play(self, i):
        self.player.play_song(f'{self.sounds_path}{i}')



def main():
    task = MentalCalc()
    task.test()


if __name__ == '__main__':
    main()