# coding: utf-8
from os import linesep
import tkinter as tk
from tkinter import ttk
import csv
import random
import time
from dataclasses import dataclass
from datetime import datetime
random.seed(0)

from baseapp import BaseFrame

class Stroop(BaseFrame):
    @dataclass
    class TaskData:
        correct: str
        choices: list
        
        def __call__(self):
            return self.correct, self.choices

    def __init__(self, task, fname=None, path=r'./', limit_cnt=None, limit_second=None):
        super().__init__()
        self.master.config(bg='light gray')
        self.master.protocol("WM_DELETE_WINDOW", self.finish)

        self.task_num = task-1
        self.tasks = [self.task1, self.task2, self.task3, self.task4]
        self.task = self.tasks[self.task_num]
        self.colors = dict(zip(['green', 'blue', 'red', 'black', 'yellow'],
                                ['みどり', 'あ お', 'あ か', 'く ろ', 'きいろ']))

        self.fpath = path
        self.fname = fname if fname else datetime.now().isoformat()
        self.cnt = 0
        self.limit_cnt = limit_cnt
        self.limit_time = limit_second
        self.start_time = time.time()
        self.output_data = []
        self.column = ['cnt', 'time', 'correct', 'answer', 'result', 'choice1', 'choice2', 'choice3', 'choice4', 'choice5', 'result']
        self.stream_data = None

        self.create_widgets()
        self.dt = 0

    def create_widgets(self):
        self.color_label = tk.Label(self,
            text='', width=10, height=2, borderwidth=2, relief=tk.SOLID,
            bg='light gray', font=('MS ゴシック', '25', 'bold')
        )

        self.color_patchs = [tk.Button(self, width=10, height=2, borderwidth=2, relief=tk.SOLID,
            font=('MS ゴシック', '15', 'bold')) for _ in range(5)]

        for i, patch in enumerate(self.color_patchs):
            func = self.patch_clicked(i)
            patch.config(command=func)

        self.task()

    def patch_clicked(self, num):
        def process():
            t = time.time()
            self.t = t - self.start_time
            self.cnt += 1
            correct, choice = self.stream_data()
            answer = choice[num]
            #result = 1 if correct == answer else 0
            self.output_data.append([self.cnt, self.t, correct, answer, int(correct==answer)] + choice)
            
            self.task()
        return process
    
    def over_limit(self):
        t = time.time()
        if self.limit_cnt and self.limit_time:
            return self.limit_time <= t - self.start_time or self.limit_cnt <= self.cnt
        elif self.limit_cnt:
            return self.limit_cnt <= self.cnt
        elif self.limit_time:
            return self.limit_time <= t - self.start_time
        else:
            return False

    def task1(self):
        '''
        逆ストループ統制課題
        黒インクで書かれた単語が意味する色をその右側の5種の色パッチの中から選ぶ．
        '''
        if self.over_limit():
            self.finish()

        self.color_label['fg'] = 'black'
        self.color_label['text'] = random.choice(list(self.colors.values()))
        self.color_label.pack(side=tk.LEFT, padx=10, anchor=tk.CENTER, fill='x')

        for patch, c in zip(self.color_patchs, random.sample(list(self.colors.keys()), len(self.colors))):
            patch['bg'] = c
            patch.pack(side=tk.LEFT, padx=10, anchor=tk.CENTER, fill='x')

        correct = [k for k, v in self.colors.items() if self.color_label.cget('text') == v][0]
        choices = [p.cget('bg') for p in self.color_patchs]
        self.stream_data = Stroop.TaskData(correct, choices)

    def task2(self):
        '''
        逆ストループ課題
        色・色名不一致語の単語が意味する色をその右側の色パッチの中から選ぶ．
        '''
        if self.over_limit():
            self.finish()
        self.color_label['fg'] = random.choice(list(self.colors.keys()))
        self.color_label['text'] = random.choice(list(self.colors.values()))
        self.color_label.pack(side=tk.LEFT, padx=10, anchor=tk.CENTER)

        for patch, c in zip(self.color_patchs, random.sample(list(self.colors), len(self.colors))):
            patch['bg'] = c
            patch.pack(side=tk.LEFT, padx=10, anchor=tk.CENTER)

        correct = self.color_label.cget('text')
        choices = [p.cget('bg') for p in self.color_patchs]
        self.stream_data = Stroop.TaskData(correct, choices)

    def task3(self):
        '''
        ストループ統制課題
        色パッチのインクの色に対する色名語を選ぶ．
        '''
        if self.over_limit():
            self.finish()
        self.color_label['bg'] = random.choice(list(self.colors.keys()))
        self.color_label['text'] = ''
        self.color_label.pack(side=tk.LEFT, padx=10, anchor=tk.CENTER)

        for patch, c in zip(self.color_patchs, random.sample(list(self.colors), len(self.colors))):
            patch['bg'] = 'light gray'
            patch['fg'] = 'black'
            patch['text'] = self.colors[c]
            patch.pack(side=tk.LEFT, padx=10, anchor=tk.CENTER)
        
        correct = self.color_label.cget('bg')
        choices = [p.cget('text') for p in self.color_patchs]
        self.stream_data = Stroop.TaskData(correct, choices)

    def task4(self):
        '''
        ストループ課題
        色・色名不一致語のインクの色に対する色名語を選ぶ
        '''
        if self.over_limit():
            self.save()
            self.finish()
        self.color_label['bg'] = 'light gray'
        self.color_label['fg'] = random.choice(list(self.colors.keys()))
        self.color_label['text'] = random.choice(list(self.colors.values()))
        self.color_label.pack(side=tk.LEFT, padx=10, anchor=tk.CENTER)
        
        for patch, c in zip(self.color_patchs, random.sample(list(self.colors), len(self.colors))):
            patch['bg'] = 'light gray'
            patch['fg'] = 'black'
            patch['text'] = self.colors[c]
            patch.pack(side=tk.LEFT, padx=10, anchor=tk.CENTER)

        correct = self.color_label.cget('fg')
        choices = [p.cget('text') for p in self.color_patchs]
        self.stream_data = Stroop.TaskData(correct, choices)

    def save(self):
        print(*self.output_data, sep='\n')
        #TODO Decide the directory for writing csv files
        fname = f'task{self.task_num+1}.csv'
        with open(self.fpath+fname, 'w', newline='') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(self.column)
            writer.writerows(self.output_data)


def main():
    task = 4
    for t in range(1, task+1):
        app = Stroop(t, fname='stroop_test', limit_cnt=5, limit_second=10)
        app.mainloop()


if __name__ == "__main__":
    main()