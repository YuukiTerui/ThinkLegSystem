import tkinter as tk
from tkinter import ttk 
import csv
from datetime import datetime


class VasFrame(tk.Frame):
    def __init__(self, master=None, fname=None, path=r'./'):
        super().__init__(master)
        self.master = master
        self.fname = fname
        self.fpath = path
        self.val = tk.DoubleVar()
        self.create_widgets()
        self.pack()

    def create_widgets(self):
        text = "今現在のあなたの疲労感について，適当な場所にマーカーを動かしてください．"
        self.question_label = tk.Label(self.master, text=text)
        self.question_label.pack()

        self.scale = ttk.Scale(
            self, variable=self.val, orient=tk.HORIZONTAL, length=600,
            from_=0, to=100,
            command=lambda e: print(f"val:{self.val.get():4}")
        )
        self.scale.pack()

        self.submit_button = tk.Button(
            self, text="Submit", command=self.submit
        )
        self.submit_button.pack()

    def submit(self):
        self.save()
        self.finish()

    def save(self):
        print(f"save value: {self.val.get()}")
        if not self.fname:
            self.fname = fr"{datetime.now().isoformat()}.csv"
        with open(self.fpath + self.fname, 'w') as f:
            writer = csv.writer(f, lineterminator=',')
            writer.writerow([self.val.get()])

    def finish(self):
        print("good bye")
        self.master.destroy()



def main():
    width = 800
    height = 600
    root = tk.Tk()
    root.title = "VAS"
    root.geometry(f"{width}x{height}")
    app = VasFrame(root, fname='vas_test')
    app.mainloop()


if __name__ == "__main__":
    main()