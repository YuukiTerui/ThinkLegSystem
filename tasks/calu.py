from os import sep
import time
import tkinter as tk
import numpy as np
from numpy.random import randint, normal, choice

from baseapp import BaseFrame

class Calc(BaseFrame):
    def __init__(self, fname=None, path='./', question_num=5):
        super().__init__()
        self._init_bind(self)
        self.is_run = False
        self.cnt = 0
        self.question_num = question_num
        self.questions = [['num_l1', '+or-', 'num_l2', '=', 'val', 'correct']]
        self.answers = [['answer', 'result', 'time']]
        
        self.create_widget()
        
    def create_widget(self):
        self.question_label = tk.Label(self, text='Ready?', relief=tk.RAISED)
        self.question_label['font'] = ('MSゴシック', 80, 'bold')
        self.question_label.config(bg=self.bg)
        self._init_bind(self.question_label)
        self.question_label.pack(expand=True, fill=tk.BOTH)
    
    def _init_bind(self, obj):
        obj.bind('<Button-1>', self.mouse_clicked)
        obj.bind('<Button-3>', self.mouse_clicked)

    def mouse_clicked(self, event):
        if not self.is_run:
            self.start_time = time.time()
            self.is_run = True
        else:
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

    def create_question(self):
        num1 = randint(low=10, high=99, size=None, dtype='I')
        symbol = choice(['+', '-'])
        num2 = randint(low=10, high=99, size=None, dtype='I')
        correct = eval(f'{num1}{symbol}{num2}')
        val = int(normal(loc=correct, scale=0.5, size=None))
        q = [num1, symbol, num2, '=', val, correct]
        self.questions.append(q)
    
    def update_label(self):
        text = ' '.join([str(x) for x in self.questions[-1][:-1]])
        self.question_label['text'] = text
    
    def save(self):
        data = [q + a for q, a in zip(self.questions, self.answers)]
        print(*data, sep='\n')




def main():
    app = Calc()
    app.mainloop()


if __name__ == '__main__':
    main()