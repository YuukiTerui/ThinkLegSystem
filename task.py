import tkinter as tk
from tasks.baseapp import BaseApp, BaseFrame
from tasks.vas import VasFrame
from tasks.calc import CalcFrame


class MainApp(BaseApp):
    def __init__(self):
        super().__init__()
        self.state = 0
        self.frame = None
        self.create_widgets()

    def create_widgets(self):
        self.frame = BaseFrame(self)
        self.frame.pack()

        self.title_label = tk.Label(self.frame, text='Think Leg System')
        self.title_label.pack()

        self.vas_button = tk.Button(self.frame, text='vas', command=lambda:self.change_frame('vas'))
        self.vas_button.pack()

        self.calc_button = tk.Button(self.frame, text='calc', command=lambda:self.change_frame('calc'))
        self.calc_button.pack()

    def create_vas(self):
        self.frame = VasFrame(self)
        self.frame.pack()


    def change_frame(self, to):
        if self.frame:
            self.frame.destroy()
        if to == 'vas':
            self.create_vas()
        elif to == 'calc':
            self.frame = CalcFrame(self)
            self.frame.pack()




def main():
    app = MainApp()
    app.mainloop()



if __name__ == '__main__':
    main()
