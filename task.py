import tkinter as tk
from tasks.baseapp import BaseApp, BaseFrame
from tasks.vas import VasFrame
from tasks.stroop import Stroop
from tasks.calu import Calc


class MainApp(BaseApp):
    def __init__(self):
        super().__init__()
        self.state = 0

    def create_widgets(self):
        self.first_frame = BaseFrame(self)
        self.first_frame.pack()

        self.title_label = tk.Label(self.first_frame, text='Think Leg System')
        self.title_label.pack()




def main():
    app = MainApp()
    app.mainloop()



if __name__ == '__main__':
    main()
