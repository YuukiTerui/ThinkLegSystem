import tkinter as tk
import json
import csv
import random
from itertools import combinations
from tkinter import font
from tkinter.constants import LEFT

from .baseframe import BaseFrame


class NasaTLX(BaseFrame):
    def __init__(self, master, path='./data/nasa_tlx/', fname='nasa_tlx.csv'):
        super().__init__(master)
        self.path = path
        self.fname = fname
        self.conf = self.load_conf()
        self.vals = [tk.IntVar(value=50) for _ in range(len(self.conf))]
        self.weight = [0] * len(self.vals)
        self.explanation = tk.StringVar()
        self.font_scale = ('MS ゴシック', 25, 'bold')
        self.font_exp = ('MS ゴシック', 18)
        self.pwc = PairWiseComparisons # 引数で変える？
        self.create_widgets()
        
    def create_widgets(self):
        title = tk.Label(self, text='NASA-TLX', font=('MS ゴシック', 50, 'bold'))
        title.pack()
        for i in range(1, len(self.conf)+1):
            frame = self.create_vas_frame(i)
            frame.pack(expand=True, fill=tk.Y, pady=20)
            #tmp.grid(column=0, row=0)
            
        exp_label = tk.Label(self, text='', textvariable=self.explanation, font=self.font_exp)
        exp_label.pack(padx=30, pady=30)
        
        pwc_btn = tk.Button(self, text='一対比較', font=self.font_scale,
            command=self.pwc_btn_clicked, padx=30, pady=30)
        pwc_btn.pack(side=tk.LEFT, anchor=tk.SE, padx=30, pady=30)

        finish_btn = tk.Button(
            self, text=" Submit ", font=self.font_scale,
            command=self.submit_clicked, padx=50, pady=30,
        )
        finish_btn.pack(side=tk.LEFT, anchor=tk.SE, padx=30, pady=30)
        
        return super().create_widgets()
    
    def create_vas_frame(self, n):
        data = self.conf[str(n)]
        frame = tk.Frame(self, relief='solid', borderwidth=1)
        title = tk.Button(frame, text=data['name_jp'], font=self.font_scale, 
                          width=15,
                          command=self.view_explanation(data['name_jp'], data['explanation']))
        #title.pack(side=tk.LEFT, padx=50, anchor=tk.CENTER)
        title.grid(column=0, row=0, padx=30, sticky=tk.W+tk.E)
        
        label_l = tk.Label(frame, text=data['min_text'], font=self.font_scale)
        #label_l.pack(side=tk.LEFT, anchor=tk.CENTER)
        label_l.grid(column=1, row=0)
        
        scale = tk.Scale(frame,
            variable=self.vals[n-1], orient=tk.HORIZONTAL, length=800, width=30,
            from_=0, to=100, showvalue=False, font=self.font_scale
        )
        #scale.pack(side=tk.LEFT, anchor=tk.CENTER)
        scale.grid(column=2, row=0)
        
        label_r = tk.Label(frame, text=data['max_text'], font=self.font_scale)
        #label_r.pack(side=tk.LEFT, anchor=tk.CENTER)
        label_r.grid(column=3, row=0)
        return frame
    
    def pwc_btn_clicked(self):
        vals = [val.get() for val in self.vals]
        window = tk.Toplevel(self.master)
        window.geometry(f'{self.master.width}x{self.master.height}')
        self.pwc(window, self, self.conf, vals)
        
    def submit_clicked(self):
        self.submit()
        self.finish()
        
    def submit(self):
        columns = [self.conf[str(i)]['name_short'] for i in range(1, len(self.conf)+1)]
        vals = [val.get() for val in self.vals]
        print(columns)
        print(vals)
        with open(self.path + self.fname, 'a', newline='') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(columns)
            writer.writerow(vals)
            writer.writerow(self.weight)
        return vals
        
    def load_conf(self):
        with open('./config/nasa_tlx_conf.json', 'r', encoding='utf-8') as f:
            conf = json.load(f)
        return conf
    
    def view_explanation(self, njp, exp):
        def change():
            self.explanation.set(f'[{njp}]={exp}')
        return change
    
    
class PairWiseComparisons(BaseFrame):
    def __init__(self, master, top, tlx, data):
        super().__init__(master)
        self.top = top
        self.tlx = tlx
        self.data = data
        self.pairs = self.create_pairs()
        self.pair = None
        self.weight = [0] * len(data)
        self.title1 = tk.StringVar()
        self.title2 = tk.StringVar()
        self.exp1 = tk.StringVar()
        self.exp2 = tk.StringVar()
        self.explanation = tk.StringVar()
        
        self.create_widgets()
        self.update()
        
    def create_widgets(self):
        exp_label = tk.Label(self, font=('MS ゴシック', 20, 'bold'),
            pady=50,
            text='今行った作業についてお聞きします．下に示す2つの項目のうち，作業負荷・負担に関りが深いと思う方をクリックしてください．')
        exp_label.grid(row=0, columnspan=2, sticky=tk.W+tk.E+tk.N+tk.S)
        
        self.btn1 = tk.Button(self, textvariable=self.title1, font=('MS ゴシック', 50, 'bold'),
            command=lambda: self.btn_clicked(0), pady=20
        )
        self.btn1.grid(row=1, column=0)
        
        self.btn2 = tk.Button(self, textvariable=self.title2,  font=('MS ゴシック', 50, 'bold'),
            command=lambda: self.btn_clicked(1), pady=20
        )
        self.btn2.grid(row=1, column=1)
        
        self.exp_btn1 = tk.Button(self, text='説明', font=('MS ゴシック', 20, 'bold'),
            command=lambda: self.explanation.set(self.exp1.get()))
        self.exp_btn1.grid(row=2, column=0)
        
        self.exp_btn2 = tk.Button(self, text='説明', font=('MS ゴシック', 20, 'bold'),
            command=lambda: self.explanation.set(self.exp2.get()))
        self.exp_btn2.grid(row=2, column=1)
        
        self.exp = tk.Label(self, textvariable=self.explanation, font=('MS ゴシック', 15, 'bold'))
        self.exp.grid(row=3, columnspan=2, sticky=tk.W+tk.E+tk.N+tk.S)
        return super().create_widgets()
    
    def create_pairs(self):
        data = [str(i) for i in range(1, len(self.data))]
        data_pair = list(combinations(data, 2))
        random.shuffle(data_pair)
        return data_pair
    
    def btn_clicked(self, n):
        self.record(n)
        self.update()
        
    def update(self):
        if not self.pairs:
            self.top.weight = self.weight
            self.finish()
        else:
            self.pair = self.pairs.pop(0)
            d1, d2 = self.pair
            self.title1.set(self.tlx[d1]['name_jp'])
            self.title2.set(self.tlx[d2]['name_jp'])
            self.exp1.set(self.tlx[d1]['explanation'])
            self.exp2.set(self.tlx[d2]['explanation'])
    
    def record(self, n):
        idx = int(self.pair[n]) - 1
        self.weight[idx] += 1
        print(self.tlx[str(idx+1)]['name_jp'])
        
    def finish(self):
        self.master.destroy()
        self.master.update()
            
        
        
            

def main():
    pass


if __name__ == '__main__':
    main()