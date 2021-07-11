import tkinter as tk
import json
from .baseframe import BaseFrame


class NasaTLX(BaseFrame):
    def __init__(self, master, fname):
        super().__init__(master)
        self.fname = fname
        self.nasa_tlx = self.load_conf()
        self.vals = [tk.IntVar() for _ in range(len(self.nasa_tlx))]
        self.explanation = tk.StringVar()
        self.create_widgets()
        
    def create_widgets(self):
        for i in range(1, len(self.nasa_tlx)+1):
            tmp = self.create_vas_frame(i)
            tmp.pack()
            
        finish_btn = tk.Button(
            self, text=" Submit ", command=self.submit, padx=50, pady=30,
        )
        finish_btn.pack(anchor=tk.SW, padx=30, pady=30)
        
        return super().create_widgets()
    
    def create_vas_frame(self, n):
        data = self.nasa_tlx[str(n)]
        frame = tk.Frame(self, )
        title = tk.Button(frame, text=data['name_jp'], command=self.view_explanation)
        title.pack(side=tk.LEFT, padx=50, pady=20)
        label_l = tk.Label(frame, text=data['min_text'])
        label_l.pack(side=tk.LEFT)
        scale = tk.Scale(frame,
            variable=self.vals[n-1], orient=tk.HORIZONTAL, length=800, width=30,
            from_=0, to=100, showvalue=False,
        )
        scale.pack(side=tk.LEFT)
        label_r = tk.Label(frame, text=data['max_text'])
        label_r.pack(side=tk.LEFT)
        return frame
    
    def submit(self):
        columns = [self.nasa_tlx[str(i)]['name_short'] for i in range(1, len(self.nasa_tlx)+1)]
        vals = [val.get() for val in self.vals]
        print(columns)
        print(vals)
        
    def load_conf(self):
        with open('./config/nasa_tlx_conf.json', 'r', encoding='utf-8') as f:
            conf = json.load(f)
        return conf
    
    def view_explanation(self):
        pass
    
def main():
    pass


if __name__ == '__main__':
    main()