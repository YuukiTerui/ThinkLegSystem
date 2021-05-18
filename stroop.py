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
        self.fname = fname if fname else datetime.now().isoformat()
        self.fpath = path

        self.master.config(bg='light gray')
        self.create_widgets()
        self.pack(anchor=tk.CENTER)

    def create_widgets(self):
        self.color_label = tk.Label(
            text='', width=10, height=2, borderwidth=2, relief=tk.SOLID,
            bg='light gray', font=('MS ゴシック', '25', 'bold')
        )
        self.color_patchs = [tk.Button(width=10, height=2, borderwidth=2, relief=tk.SOLID,
            font=('MS ゴシック', '15', 'bold')) for _ in range(5)]
        for i, patch in enumerate(self.color_patchs):
            func = self.patch_clicked(patch, i)
            patch.config(command=func)
        self.task()

    def patch_clicked(self, button, num):
        def process():
            print(num)
            self.task()
        return process

    def task1(self):
        '''
        逆ストループ統制課題
        黒インクで書かれた単語が意味する色をその右側の5種の色パッチの中から選ぶ．
        '''
        self.color_label['fg'] = 'black'
        self.color_label['text'] = random.choice(list(self.colors.values()))
        self.color_label.pack(side=tk.LEFT, padx=10, anchor=tk.CENTER, fill='x')
        for patch, c in zip(self.color_patchs, random.sample(list(self.colors.keys()), len(self.colors))):
            patch['bg'] = c
            patch.pack(side=tk.LEFT, padx=10, anchor=tk.CENTER, fill='x')

    def task2(self):
        '''
        逆ストループ課題
        色・色名不一致語の単語が意味する色をその右側の色パッチの中から選ぶ．
        '''
        self.color_label['fg'] = random.choice(list(self.colors.keys()))
        self.color_label['text'] = random.choice(list(self.colors.values()))
        self.color_label.pack(side=tk.LEFT, padx=10, anchor=tk.CENTER)
        for patch, c in zip(self.color_patchs, random.sample(list(self.colors), len(self.colors))):
            patch['bg'] = c
            patch.pack(side=tk.LEFT, padx=10, anchor=tk.CENTER)

    def task3(self):
        '''
        ストループ統制課題
        色パッチのインクの色に対する色名語を選ぶ．
        '''
        self.color_label['bg'] = random.choice(list(self.colors.keys()))
        self.color_label['text'] = ''
        self.color_label.pack(side=tk.LEFT, padx=10, anchor=tk.CENTER)
        for patch, c in zip(self.color_patchs, random.sample(list(self.colors), len(self.colors))):
            patch['bg'] = 'light gray'
            patch['fg'] = 'black'
            patch['text'] = self.colors[c]
            patch.pack(side=tk.LEFT, padx=10, anchor=tk.CENTER)

    def task4(self):
        '''
        ストループ課題
        色・色名不一致語のインクの色に対する色名語を選ぶ
        '''
        self.color_label['bg'] = 'light gray'
        self.color_label['fg'] = random.choice(list(self.colors.keys()))
        self.color_label['text'] = random.choice(list(self.colors.values()))
        self.color_label.pack(side=tk.LEFT, padx=10, anchor=tk.CENTER)
        for patch, c in zip(self.color_patchs, random.sample(list(self.colors), len(self.colors))):
            patch['bg'] = 'light gray'
            patch['fg'] = 'black'
            patch['text'] = self.colors[c]
            patch.pack(side=tk.LEFT, padx=10, anchor=tk.CENTER)


    def save(self):
        pass

    def finish(self):
        print("good bye")
        self.master.destroy()



def main():
    width = 1200
    height = 800
    
    task = 1
    for task in range(1, 2):
        root = tk.Tk()
        root.title = "Stroop"
        root.geometry(f"{width}x{height}")
        app = StroopFrame(task, master=root,fname='stroop_test')
        app.mainloop()


if __name__ == "__main__":
    main()