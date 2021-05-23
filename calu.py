from datetime import time
import tkinter as tk
import numpy as np
from numpy.random import randint, normal, choice

from baseapp import BaseFrame

class Calc(BaseFrame):
    def __init__(self, fname=None, path='./', question_num=0):
        super().__init__()
        self._init_bind()
        self.cnt = 0
        self.question_num = question_num
        self.questions = [['num_l1', '+or-', 'num_l2', '=', 'val', 'correct']]
        self.answers = [['answer', 'true-false', 'time']]
        
        self.create_widget()
        

    def create_widget(self):
        

        self.question_label = tk.Label(self, text='Ready?', relief=tk.RAISED)
        self.question_label['font'] = ('MSゴシック', 60, 'bold')
        self.question_label.pack(expand=True)

        self.config(bg='light gray')
        self.pack(fill=tk.BOTH, expand=True)

    
    def _init_bind(self):
        self.master.bind('<Button-1>', self.mouse_clicked)
        self.master.bind('<Button-3>', self.mouse_clicked)

    def mouse_clicked(self, event):
        print(event)
        self.create_question()
        self.update_label()

    def create_question(self):
        num1 = randint(low=10, high=99, size=None, dtype='I')
        symbol = choice(['+', '-'])
        num2 = randint(low=10, high=99, size=None, dtype='I')
        correct = eval(f'{num1}{symbol}{num2}')
        val = int(normal(loc=correct, scale=0.5, size=None))
        q = [num1, symbol, num2, '=', val]
        self.questions.append(q)
    
    def update_label(self):
        text = ' '.join([str(x) for x in self.questions[-1]])
        print(text)
        self.question_label['text'] = text



def main():
    app = Calc()
    app.mainloop()


if __name__ == '__main__':
    main()