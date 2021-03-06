# coding: utf-8
from os import sep
import csv
import time
import tkinter as tk
import numpy as np
from numpy.random import randint, normal, choice
from datetime import datetime

from .baseframe import BaseFrame

class CalcFrame(BaseFrame):
    def __init__(self, master=None, fname=None, path='./', question_num=5):
        super().__init__(master)
        self._init_bind(self)
        self.path = path
        self.fname = fname
        self.is_running = False
        self.cnt = 0
        self.question_num = question_num
        self.questions = [['num_l1', '+or-', 'num_l2', '=', 'val', 'correct']]
        self.answers = [['answer', 'result', 'time']]
        
        self.create_widgets()
        
    def create_widgets(self):
        self.question_label = tk.Label(self, text='Ready?', relief=tk.RAISED)
        self.question_label['font'] = ('MSゴシック', 80, 'bold')
        self.question_label.config(bg=self.bg)
        self._init_bind(self.question_label)
        self.question_label.pack(expand=True, fill=tk.BOTH)
        self.logger.debug("widgets are created.")
    
    def _init_bind(self, obj):
        obj.bind('<Button-1>', self.mouse_clicked)
        obj.bind('<Button-3>', self.mouse_clicked)
        self.logger.debug("binds are initilized.")

    def mouse_clicked(self, event):
        self.logger.debug("mouse clicked. %s", event)
        if not self.is_running:
            self.logger.debug("is_running == %s", self.is_running)
            self.start_time = time.time()
            self.is_running = True
        else:
            self.logger.debug("is_run == %s", self.is_running)
            ans = 1 if event.num == 1 else 0
            t = time.time() - self.start_time
            self.record_answer(ans, t)
            self.cnt += 1
            if self.cnt == self.question_num:
                self.save()
                self.finish()
                return
        
        self.create_question()
        self.update_label()

    def record_answer(self, ans, t):
        q = self.questions[-1]
        result = (q[-1]==q[-2]) == ans
        self.answers.append([ans, result, t])
        self.logger.debug("answer is recorded.")

    def create_question(self):
        num1 = randint(low=10, high=99, size=None, dtype='I')
        symbol = choice(['+', '-'])
        num2 = randint(low=10, high=99, size=None, dtype='I')
        correct = eval(f'{num1}{symbol}{num2}')
        val = int(normal(loc=correct, scale=0.5, size=None))
        q = [num1, symbol, num2, '=', val, correct]
        self.questions.append(q)
        self.logger.debug("question is created.%s", q)
    
    def update_label(self):
        text = ' '.join([str(x) for x in self.questions[-1][:-1]])
        self.question_label['text'] = text
        self.logger.debug("label is updated.")
    
    def save(self):
        data = [q + a for q, a in zip(self.questions, self.answers)]
        if not self.fname:
            self.fname = f'{datetime.now().isoformat()}.csv'
        with open(f'{self.path}{self.fname}', 'a', newline='') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerows(data)
        self.logger.info("data is saved %s", self.fname)




def main():
    app = CalcFrame(fname='calc.csv')
    app.mainloop()


if __name__ == '__main__':
    main()