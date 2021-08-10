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

        self.startnum = startnum
        self.endnum = endnum
        self.currentnum = IntVar(value=startnum)

        self.create_widgets()

    def create_widgets(self):
        self.currentnum_label = Label(self, textvariable=self.currentnum, font=('', 30))
        self.currentnum_label.pack()

        self.number_markers = self.NumberMarker(self, self.startnum, self.endnum)
        self.number_markers.pack(padx=50, pady=50)

        return super().create_widgets()

    class NumberMarker(Canvas):
        def __init__(self, master, startnum, endnum):
            super().__init__(master=master,
            width=1200,
            height=800
            )
            self.startnum = startnum
            self.endnum = endnum
            self.border = 0
            self.borderwidth = 0
            self.oval_diameter = 40
            self.bind('<ButtonPress-1>', self.__on_press)
            self.bind('<ButtonRelease-1>', self.__on_release)

        def draw(self, n):
            points = []
            for i in range(5):
                for j in range(5):
                    x = randint(i*self.width/5, (i+1)*self.width/5)
                    y = randint(j*self.height/5, (j+1)*self.height/5)
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
                self.itemconfig(id, fill='red')
            return inner
            
        def __leave(self, id):
            def inner(event):
                self.itemconfig(id, fill='gray')
            return inner

        def __on_press(self, event):
            x, y = self.canvasx(event.x),  self.canvasy(event.y)
            l = [self.itemcget(obj,'tags') for obj in self.find_overlapping(x, y, x, y)]
            print(datetime.now(), 'press', l, x, y)

        def __on_release(self, event):
            x, y = self.canvasx(event.x),  self.canvasy(event.y)
            l = [self.itemcget(obj,'tags') for obj in self.find_overlapping(x, y, x, y)]
            print(datetime.now(), 'release', l, x, y)
            self.update()

        def update(self):
            n = self.master.currentnum.get()
            if n == self.endnum:
                pass
                # TODO finish()
            else:
                self.master.currentnum.set(n+1)
                self.draw(n+1)
