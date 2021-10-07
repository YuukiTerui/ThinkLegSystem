import csv
from datetime import datetime
from random import randint, sample, shuffle
import tkinter as tk
from tkinter import Canvas, IntVar, Label

from tasks.frames.baseframe import BaseFrame

class ATMTFrame(BaseFrame):
    def __init__(self, master, path='./data/ATMT/', fname='atmt.csv', startnum=11, endnum=45):
        super().__init__(master)
        self.path = path
        self.fname = fname
        self.is_running = False
        self.width = master['width']
        self.height = master['height']
        self.records = []

        self.startnum = startnum
        self.endnum = endnum
        self.currentnum = IntVar(value=startnum)

        self.create_widgets()

    def create_widgets(self):
        self.screen_label = Label(self, text='クリックで開始')
        self.screen_label.bind('<ButtonRelease-1>', self.__start)
        self.screen_label.pack(expand=True, fill=tk.BOTH)

        return super().create_widgets()

    def __start(self, event):
        self.screen_label.destroy()
        frame = TaskFrame(self, startnum=self.startnum, endnum=self.endnum)
        frame.pack()

    def to_csv(self, path=None, fname=None, n=-1):
        if self.records is None:
            return
        if path is None:
            path = self.path
        if fname is None:
            fname = self.fname

        with open(path+fname, 'a', newline='\n') as f:
            writer = csv.writer(f)
            writer.writerows(self.records[n])
      


class TaskFrame(BaseFrame):
    def __init__(self, master, **args) -> None:
        super().__init__(master=master)
        self.startnum = args['startnum']
        self.endnum = args['endnum']
        self.record = [] # [datetime, num, correction]
        self.currentnum = self.startnum
        self.create_widgets()
        self.draw2()
        self.starttime = datetime.now()

    def create_widgets(self):
        self.current_num_label = Label(self, text=self.currentnum, font=('', 30))
        self.current_num_label.pack()

        self.canvas_w = 800
        self.canvas_h = 600
        self.canvas_items = [] # idが入る [(oval_id, text_id), ...]
        self.canvas = Canvas(self, bg='light gray', width=self.canvas_w, height=self.canvas_h)
        self.canvas.pack()

    def draw2(self):
        cn = self.currentnum
        nums = sample(list(range(cn, cn+25)), 25)
        points = sample(list(range(0, 48)), 25)
        oval_size = 40
        for n, p in zip(nums, points):
            x0 = (p - (p // 8 * 8)) * 100
            y0 = (p // 8) * 100
            x0 = randint(x0, x0+100-oval_size)
            y0 = randint(y0, y0+100-oval_size)
            oval = self.canvas.create_oval(x0, y0, x0+oval_size, y0+oval_size, fill='gray', activefill='light gray', tags=n)
            oval_text = self.canvas.create_text(x0+oval_size//2, y0+oval_size//2, text=n, font=('', 14), fill='black', tags=n)
            self.canvas.tag_bind(oval_text, '<Enter>', self.__enter(oval))
            self.canvas.tag_bind(oval_text, '<Leave>', self.__leave(oval))
            self.canvas.tag_bind(oval_text, '<Button-1>', self.__clicked)
            self.canvas.tag_bind(oval, '<Button-1>', self.__clicked)

    def __enter(self, id):
        def inner(event):
            self.canvas.itemconfig(id, fill='light gray')
        return inner

    def __leave(self, id):
        def inner(event):
            self.canvas.itemconfig(id, fill='gray')
        return inner

    def __clicked(self, event):
        x, y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        tags = [self.canvas.itemcget(obj, 'tags') for obj in self.canvas.find_overlapping(x, y, x, y)]

        t = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        correction = self.correct(tags)
        self.record.append([t, self.currentnum, correction])

        self.update()

    def correct(self, tags):
        if set([f'{self.currentnum}', f'{self.currentnum} current']) & set(tags):
            return True
        return False

    def clean_canvas(self):
        self.canvas.addtag_all('delete')
        self.canvas.delete('delete')

    def update(self):
        if self.currentnum < self.endnum:
            self.clean_canvas()
            self.currentnum += 1
            self.current_num_label.config(text=self.currentnum)
            self.draw2()
        else:
            print(*self.record, sep='\n')
            self.save()
            self.finish()

    def save(self):
        self.master.records.append(self.record)
        self.master.to_csv()

    def finish(self):
        self.master.finish()