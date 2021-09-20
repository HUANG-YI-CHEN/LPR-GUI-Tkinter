import logging
import os
import time
import tkinter as tk
from time import strftime
from tkinter import ttk

from lib.logger import Logger
from lib.tab_frame1 import TabFrame_1
from lib.tab_frame3 import TabFrame_3

debug_level = logging.INFO
logging.basicConfig(**Logger(debug_level, False).config())
# logging.disable(logging.INFO)

class GUI_LPR(tk.Frame):
    def __init__(self, win):
        super(GUI_LPR, self).__init__(win)
        self.win = win
        self.win.protocol("WM_DELETE_WINDOW", lambda e=None:self.destroy_window(e))
        self.set_center_geometry(self.win)

        self.parms = [
            {'tab': {'text': 'Demo Tab', 'bg': '#fae3dc', 'fill':'both', 'expand':True, 'state':'normal'}},
            {'tab': {'text': 'Train Tab', 'bg': '#fae3dc', 'fill':'both', 'expand':True, 'state':'disable'}},
            {'tab': {'text': 'Report Tab', 'bg': '#fae3dc', 'fill':'both', 'expand':True, 'state':'normal'}},
        ] # yapf:disable
        parms = self.parms
        self.tab = []
        notebook = ttk.Notebook(win)
        notebook.pack(expand=True, fill='both', side='top')
        for idx, parm in enumerate(self.parms):
            bg = parm['tab']['bg']
            self.tab.append(tk.Frame(notebook, bg=bg))
        for idx, tab in enumerate(self.tab):
            fill = parms[idx]['tab']['fill']
            expand = parms[idx]['tab']['expand']
            tab.pack(fill=fill, expand=expand)
        for idx, tab in enumerate(self.tab):
            text = parms[idx]['tab']['text']
            state = parms[idx]['tab']['state']
            notebook.add(tab, text=' '* 10 + text + ' '*10, state=state)

        self.tab_1 = TabFrame_1(self.win, self.tab[0])
        self.tab_3 = TabFrame_3(self.tab[2])

    def set_center_geometry(self, win: tk.Tk):
        ''' 取得視窗大小和視窗位置 '''
        self.win.update()
        screen_width = win.winfo_screenwidth()
        screen_height = win.winfo_screenheight()
        width, height = win.winfo_width(), win.winfo_height()
        x = int((screen_width - width) / 2)
        y = int((screen_height - height) / 2)
        size = '%dx%d+%d+%d' % (width, height, x, y)
        self.win.geometry(size)
        self.win.update()

    def destroy_window(self, event):
        logging.info(":The LPR-GUI window has been destroyedThe LPR-GUI window has been destroyed.")
        if self.tab_3.sqlconn:
            self.tab_3.sqlconn.close()
        self.win.destroy()

def main():
    win = tk.Tk()
    win.geometry("1024x768")
    win.title('License Plate Recognition')
    glpr = GUI_LPR(win)
    win.mainloop()

if __name__ == '__main__':
    main()
