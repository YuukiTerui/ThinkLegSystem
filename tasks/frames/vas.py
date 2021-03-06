# coding: utf-8
import tkinter as tk
from tkinter import messagebox
import csv

from .baseframe import BaseFrame


class VasFrame(BaseFrame):
    def __init__(self, master=None, path='./', fname='vas.csv'):
        super().__init__(master)
        self.fname = fname
        self.fpath = path
        self.val = tk.IntVar(self.master, 50)
        self.create_widgets()
        

    def create_widgets(self):
        font = [("MSゴシック", "15", "bold"), ("MSゴシック", "10", "bold"), ("MSゴシック", "5", "bold")]
        question = "今現在のあなたの疲労感について，適当な場所にマーカーを動かしてください．"
        self.question_label = tk.Label(self, 
            text=question, font=font[0],

        )
        self.question_label.pack(pady=30, fill=tk.X, expand=True)

        self.scale_frame = tk.Frame(self, relief=tk.RAISED)
        self.scale_label_min = tk.Label(self.scale_frame,
            text='疲労感はない', font=font[1],
        )
        self.scale_label_min.pack(side=tk.LEFT)

        self.scale = tk.Scale(self.scale_frame,
            variable=self.val, orient=tk.HORIZONTAL, length=800, width=30,
            from_=0, to=100, showvalue=False,
        )
        self.scale.pack(side=tk.LEFT)

        self.scale_label_max = tk.Label(self.scale_frame,
            text='想像しうる\n最大の疲労感', font=font[1]
        )
        self.scale_label_max.pack(side=tk.LEFT)

        self.scale_frame.pack(pady=20, expand=True)

        self.submit_button = tk.Button(
            self, text=" Submit ", command=self.submit, font=font[0],
            padx=50, pady=30,
        )
        self.submit_button.pack(anchor=tk.SE, side=tk.RIGHT, fill=tk.X, padx=30, pady=30)

    def submit(self):
        ret = messagebox.askyesno('確認','提出しますか？')
        if ret == True:
            self.logger.info('submit vas.')
            self.save()
            self.finish()

    def save(self):
        self.logger.info('save value: %s', self.val.get())
        if '.csv' not in self.fname:
            self.fname += '.csv'
        with open(f'{self.fpath}{self.fname}', 'a', newline='') as f:
            writer = csv.writer(f, lineterminator=',')
            writer.writerow([self.val.get()])




def main():
    app = VasFrame(fname='vas_test.csv')
    app.mainloop()


if __name__ == "__main__":
    main()