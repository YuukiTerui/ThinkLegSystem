import tkinter as tk
from tkinter import ttk 
import csv
import random
from datetime import datetime
random.seed(0)

class StroopFrame(tk.Frame):
    def __init__(self, task, master=None, fname=None, path=r'./'):
        super().__init__(master)
        self.master = master
        self.task_num = task-1
        self.tasks = [self.task1, self.task2, self.task3, self.task4]
        self.task = self.tasks[self.task_num]
        self.colors = dict(zip(['green', 'blue', 'red', 'black', 'yellow'],
                                ['みどり', 'あ　お', 'あ　か', 'く　ろ', 'きいろ']))
        self.fname = fname
        self.fpath = path
        self.create_widgets()
        self.pack(anchor=tk.CENTER)

    def create_widgets(self):
        self.color_label = tk.Label(text='label', font=('MS ゴシック', '25', 'bold'))
        self.color_patchs = [tk.Button(width=20, height=3, command=self.task)
                            for _ in range(5)]
        self.task()
    
    def task1(self):
        '''
        逆ストループ統制課題
        黒インクで書かれた単語が意味する色をその右側の5種の色パッチの中から選ぶ．
        '''
        self.color_label['fg'] = 'black'
        self.color_label['text'] = random.choice(list(self.colors.values()))
        self.color_label.pack(side=tk.LEFT, padx=10, anchor=tk.CENTER)
        for panel, c in zip(self.color_patchs, random.sample(list(self.colors), len(self.colors))):
            panel['bg'] = c
            panel.pack(side=tk.LEFT, padx=10, anchor=tk.CENTER)

    def task2(self):
        '''
        逆ストループ課題
        色・色名不一致語の単語が意味する色をその右側の色パッチの中から選ぶ．
        '''

    def task3(self):
        '''
        ストループ統制課題
        色パッチのインクの色に対する色名語を選ぶ．
        '''

    def task4(self):
        '''
        ストループ課題
        色・色名不一致語のインクの色に対する色名語を選ぶ
        '''
        


    def save(self):
        pass

    def finish(self):
        print("good bye")
        self.master.destroy()



def main():
    width = 1200
    height = 800
    root = tk.Tk()
    root.title = "Stroop"
    root.geometry(f"{width}x{height}")
    app = StroopFrame(1, master=root,fname='stroop_test')
    app.mainloop()


if __name__ == "__main__":
    main()