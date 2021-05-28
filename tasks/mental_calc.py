# coding: utf-8

import os
import random
import time
import schedule
import tkinter as tk
from random import choices
from mpyg321.mpyg321 import MPyg321Player

from baseapp import BaseFrame


class MentalCalc(BaseFrame):
    def __init__(self):
        super().__init__()
        self.sounds_path = './sounds/'
        self.sounds = sorted(os.listdir(self.sounds_path))
        self.player = MPyg321Player()
        self.datas = []

    def sound_test(self):
        for i in range(10):
            self.play(i)
            time.sleep(1)

    def play(self, i):
        print(f'play {self.sounds_path}{self.sounds[i]}')
        self.player.play_song(f'{self.sounds_path}{self.sounds[i]}')

    def task(self):
        nums = choices(list(range(10)), k=4)
        print(nums)
        correct_num = sum(nums)
        question_num = None
        
        def question(i):
            self.play(i)
            return time.time()

        def answer():
            return time.time()

        def result():
            pass

        def process(qnum=len(nums), interval=4):
            for i in range(qnum):
                time.sleep(interval)
                question(nums[i])
            answer()

        process()


def main():
    app = MentalCalc()
    app.mainloop()

if __name__ == '__main__':
    main()