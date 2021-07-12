import tkinter as tk
import json
from .baseframe import BaseFrame


class NasaTLX(BaseFrame):
    def __init__(self, master, fname):
        super().__init__(master)
        self.fname = fname
        self.conf = self.load_conf()
        self.vals = [tk.IntVar() for _ in range(len(self.conf))]
        self.explanation = tk.StringVar()
        self.font_scale = ('MS ゴシック', 20, 'bold')
        self.font_exp = ('MS ゴシック', 10)
        self.create_widgets()
        
    def create_widgets(self):
        for i in range(1, len(self.conf)+1):
            tmp = self.create_vas_frame(i)
            tmp.pack(expand=True, fill=tk.BOTH)
            
        exp_label = tk.Label(self, text='', textvariable=self.explanation, font=self.font_exp)
        exp_label.pack(padx=30, pady=30)

        finish_btn = tk.Button(
            self, text=" Submit ", font=self.font_scale,
            command=self.submit, padx=50, pady=30,
        )
        finish_btn.pack(anchor=tk.SE, padx=30, pady=30)
        
        return super().create_widgets()
    
    def create_vas_frame(self, n):
        data = self.conf[str(n)]
        frame = tk.Frame(self, )
        title = tk.Button(frame, text=data['name_jp'], font=self.font_scale, command=self.view_explanation(data['name_jp'], data['explanation']))
        title.pack(side=tk.LEFT, padx=50, anchor=tk.CENTER)
        label_l = tk.Label(frame, text=data['min_text'], font=self.font_scale)
        label_l.pack(side=tk.LEFT, anchor=tk.CENTER)
        scale = tk.Scale(frame,
            variable=self.vals[n-1], orient=tk.HORIZONTAL, length=800, width=30,
            from_=0, to=100, showvalue=False, font=self.font_scale
        )
        scale.pack(side=tk.LEFT, anchor=tk.CENTER)
        label_r = tk.Label(frame, text=data['max_text'], font=self.font_scale)
        label_r.pack(side=tk.LEFT, anchor=tk.CENTER)
        return frame
    
    def submit(self):
        columns = [self.conf[str(i)]['name_short'] for i in range(1, len(self.conf)+1)]
        vals = [val.get() for val in self.vals]
        print(columns)
        print(vals)
        
    def load_conf(self):
        with open('./config/nasa_tlx_conf.json', 'r', encoding='utf-8') as f:
            conf = json.load(f)
        return conf
    
    def view_explanation(self, njp, exp):
        def change():
            self.explanation.set(f'[{njp}]={exp}')
        return change
    
def main():
    pass


if __name__ == '__main__':
    main()