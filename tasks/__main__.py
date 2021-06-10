# coding: utf-8
import os
from datetime import datetime

from .apps.taskapp import Tasks


def main():
    datapath = f'./data/{datetime.now().strftime("%Y%m%d/%H-%M-%S")}/'
    os.makedirs(datapath, exist_ok=True)
    app = Tasks(datapath)
    app.mainloop()

if __name__ == '__main__':
    main()