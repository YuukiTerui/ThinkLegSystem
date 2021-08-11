import csv
from datetime import datetime
from random import randint, sample, shuffle
import tkinter as tk
from tkinter import Canvas, IntVar, Label

from tasks.frames.baseframe import BaseFrame

class ATMTFrame(BaseFrame):
    def __init__(self, master, path='./data/ATMT/', fname='atmt.csv', startnum=1, endnum=25):
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
        self.currentnum_label = Label(self, textvariable=self.currentnum, font=('', 30))
        self.number_markers = self.NumberMarker(self, self.startnum, self.endnum)
        self.currentnum_label.pack()
        self.number_markers.pack(padx=50, pady=50)
        
    def save(self):
        with open(self.path + self.fname, 'a', newline='') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerows(self.records)
        
    def finish(self):
        self.destroy()

    class NumberMarker(Canvas):
        def __init__(self, master, startnum, endnum):
            self.width = 800
            self.height = 600
            super().__init__(master=master,
            width=self.width,
            height=self.height
            )
            self.startnum = startnum
            self.endnum = endnum
            self.border = 0
            self.borderwidth = 0
            self.oval_diameter = 40
            self.bind('<ButtonPress-1>', self.__on_press)
            self.bind('<ButtonRelease-1>', self.__on_release)
            self.draw(self.startnum)

        def draw(self, n):
            points = []
            for i in range(5):
                for j in range(5):
                    x = randint(i*self.width/5, (i+1)*self.width/5 - self.oval_diameter)
                    y = randint(j*self.height/5, (j+1)*self.height/5 - self.oval_diameter)
                    points.append((x, y))
            nls = sample(list(range(n, n+25)), 25)
            for (x, y), n in zip(points, nls):
                oval = self.create_oval((x, y, x+self.oval_diameter, y+self.oval_diameter),
                    outline='gray', fill='gray', width=3, tags=n)
                self.tag_bind(oval, '<Enter>', self.__enter(oval))
                self.tag_bind(oval, '<Leave>', self.__leave(oval))
                text = self.create_text(x+self.oval_diameter//2, y+self.oval_diameter//2,
                    text=n, font=('', 15))
                self.tag_bind(text, '<Enter>', self.__enter(oval))
                self.tag_bind(text, '<Leave>', self.__leave(oval))

        def __enter(self, id):
            def inner(event):
                self.itemconfig(id, fill='light gray')
            return inner
            
        def __leave(self, id):
            def inner(event):
                self.itemconfig(id, fill='gray')
            return inner

        def __on_press(self, event):
            x, y = self.canvasx(event.x),  self.canvasy(event.y)
            l = ''.join([self.itemcget(obj,'tags') for obj in self.find_overlapping(x, y, x, y)])

        def __on_release(self, event):
            x, y = self.canvasx(event.x),  self.canvasy(event.y)
            l = ''.join([self.itemcget(obj,'tags') for obj in self.find_overlapping(x, y, x, y)])
            print(datetime.now(), 'release', str(self.master.currentnum.get())in l)
            self.master.records.append(f'{datetime.now()},')
            self.update()

        def update(self):
            print('update')
            n = self.master.currentnum.get()
            if n == self.endnum:
                self.finish()
            else:
                self.delete('all')
                self.master.currentnum.set(n+1)
                self.draw(n+1)    
                
        def finish(self):
            self.master.save()
            self.master.finish()