import csv
import logging
import os
import random
import string
import time
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as msgbox
from tkinter import ttk

import cv2
from PIL import Image, ImageTk

try:
    from lib.sqlite2crud import LPR_SQL
    from lib.sqlite2crud import Sqlite2CRUD as sqlcrud
except:
    from sqlite2crud import LPR_SQL
    from sqlite2crud import Sqlite2CRUD as sqlcrud

class ScrolledTreeview(tk.Frame):
    def __init__(self, parent=None, style=None, x=0, y=0,*args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.style = style
        self.x = x
        self.y = y
        self.parent.columnconfigure(self.x, weight=1)
        self.parent.rowconfigure(self.y, weight=1)
        self.__treeview = ttk.Treeview(self.parent, style="Custom.Treeview")
        # self.__treeview = ttk.Treeview(self.parent)
        self.__treeview.grid(column=self.x, row=self.y, sticky='nsew', columnspan=2)

        self.__xscrbar = ttk.Scrollbar(self.parent, orient='horizontal')
        self.__xscrbar.grid(column=self.x, row=self.y+1, sticky='swe')
        self.__yscrbar = ttk.Scrollbar(self.parent, orient='vertical')
        self.__yscrbar.grid(column=self.x+1, row=self.y, sticky='nse')

        self.__xscrbar.config(command=self.__treeview.xview)
        self.__yscrbar.config(command=self.__treeview.yview)
        self.__treeview.configure(xscrollcommand=self.__xscrbar.set, yscrollcommand=self.__yscrbar.set)

    def csv2Treeview(self, col_name, col_heading, rows):
        self.__treeview.configure(columns=col_name, show='headings')

        # 設置列寬度
        for _, col in enumerate(col_name):
            self.__treeview.column(col, minwidth=100, width=50, stretch=True, anchor='n')
        # 添加列名稱顯示
        if len(col_heading) == len(col_name):
            for idx, col in enumerate(col_heading):
                self.__treeview.heading(col_name[idx], text=col)
        else:
            logging.info(':col_name array size != col_heading array size')
            return
        # 添加表格數據
        for _, row in enumerate(rows):
            temp = [str(row[0]).zfill(10)] + row[1:]
            self.__treeview.insert('', 'end', values=temp, tag='gray')
        self.__treeview.tag_configure('gray', background='#cccccc')

        for idx, col in enumerate(col_name):
            self.__treeview.heading(col, text=col_heading[idx], command=lambda _col=col: self.__sort_column(_col, False))

    def sql2Treeview(self, col_name, col_heading, rows):
        self.__treeview.configure(columns=col_name, show='headings')

        # 設置列寬度
        for _, col in enumerate(col_name):
            self.__treeview.column(col, minwidth=100, width=50, stretch=True, anchor='n')
        # 添加列名稱顯示
        if len(col_heading) == len(col_name):
            for idx, col in enumerate(col_heading):
                self.__treeview.heading(col_name[idx], text=col)
        else:
            logging.info(':col_name array size != col_heading array size')
            return
        # 添加表格數據
        for _, row in enumerate(rows):
            temp = (*(), str(row[0]).zfill(10)) + row[1:]
            self.__treeview.insert('', 'end', values=temp, tag='gray')
        self.__treeview.tag_configure('gray', background='#cccccc')

        for idx, col in enumerate(col_name):
            self.__treeview.heading(col, text=col_heading[idx], command=lambda _col=col: self.__sort_column(_col, False))

    def __sort_column(self, column, reverse):
        l = [(self.__treeview.set(k, column), k) for k in self.__treeview.get_children('')]
        # logging.info(':'+self.__treeview.get_children(''))
        l.sort(reverse=reverse) #排序方式
        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l): #根據排序後索引移動
            self.__treeview.move(k, '', index)
        self.__treeview.heading(column, command=lambda: self.__sort_column(column, not reverse)) #重寫標題，使之成為再點倒序的標題

class TabFrame_3:
    def __init__(self, TabFrame):
        self.tab3 = TabFrame
        self.file_path = ''
        self.sqlconn = None
        self.style = ttk.Style()
        self.style.element_create("Custom.Treeheading.border", "from", "default")
        self.style.layout("Custom.Treeview.Heading", [
            ("Custom.Treeheading.cell", {'sticky': 'nswe'}),
            ("Custom.Treeheading.border", {'sticky':'nswe', 'children': [
                ("Custom.Treeheading.padding", {'sticky':'nswe', 'children': [
                    ("Custom.Treeheading.image", {'side':'right', 'sticky':''}),
                    ("Custom.Treeheading.text", {'sticky':'we'})
                ]})
            ]}),
        ])
        self.style.configure("Custom.Treeview.Heading", background="blue", foreground="white", relief="flat")
        self.style.map("Custom.Treeview.Heading", relief=[('active','groove'),('pressed','sunken')])

        frame = tk.Frame(master=self.tab3)
        frame.grid(column=0, row=0, sticky='nsew', pady=5, columnspan=2)

        self.cbbox = ttk.Combobox(master=frame, values=['report csv','report sql'], state='readonly')
        self.cbbox.current(0)
        self.cbbox.pack(anchor='n', side='left', fill='both')
        self.img = Image.open(os.path.join(os.curdir,'icon','folder-home-open.png')).resize((20,20),Image.ANTIALIAS)
        self.imgtk = ImageTk.PhotoImage(self.img)
        self.btn = tk.Button(master=frame, image=self.imgtk, width=20, height=20, borderwidth=2)
        self.btn.config(command=(lambda:self.btn_open_select()))
        self.btn.pack(anchor='n', side='left', padx=20, fill='both')

        self.textEntry = tk.StringVar()
        self.entry = tk.Entry(master=frame, textvariable=self.textEntry)
        self.entry.pack(anchor='n', side='left', expand=True,fill='both')
        self.cbbox_select_changed(None)
        self.cbbox.bind('<<ComboboxSelected>>', (lambda e=None: self.cbbox_select_changed(e)) )

    def cbbox_select_changed(self, event):
        self.__treeview = None
        tree_column = []
        tree_heading = ['流水號', '資料夾', '檔名', '檔案類型', '辨識方式', '辨識結果', '顏色', '正確判斷', '人工修正', '辨識時間' ]
        tree_rows = []

        if self.cbbox.current() == 0:
            if self.sqlconn is not None:
                self.sqlconn.close()
                self.sqlconn = None
            self.__treeview = ScrolledTreeview(parent=self.tab3, style=self.style, x=0, y=1)
            if not os.path.exists(self.file_path) or self.file_path.find('.csv') <= 0:
                self.file_path = os.path.join(os.path.abspath(os.path.curdir),'source','example.csv')
                self.file_path = os.path.realpath(self.file_path)
            if not os.path.exists(self.file_path):
                self.clearCSV(self.file_path)
                self.testCSV(self.file_path, 30)
            with open(file=self.file_path, mode='r+', encoding='utf_8_sig') as f:
                reader = csv.reader(f)
                tree_column = [i.strip() for i in next(reader)]
                tree_rows = [[x.strip() for x in row] for row in reader]
                self.__treeview.csv2Treeview(tree_column, tree_heading, tree_rows)
        elif self.cbbox.current() == 1:
            self.__treeview = ScrolledTreeview(parent=self.tab3, style=self.style, x=0, y=1)
            if not os.path.exists(self.file_path) or self.file_path.find('.db') <= 0:
                self.file_path = os.path.join(os.path.abspath(os.path.curdir),'source','example.db')
                self.file_path = os.path.realpath(self.file_path)
            if not os.path.exists(self.file_path):
                sqlconn = sqlcrud(self.file_path)
                lpr_sql = LPR_SQL(sqlconn)
                self.clearDB(lpr_sql)
                self.testDB(lpr_sql)
                sqlconn.close()
            if self.file_path.find('.db')>0:
                self.sqlconn = sqlcrud(self.file_path)
                tree_column = self.getDBcolumns('vd_info')
                tree_rows = self.getDBrows('vd_info', -1)
                self.__treeview.sql2Treeview(tree_column, tree_heading, tree_rows)
        self.textEntry.set('【Path】＃ ' + self.file_path)

    def btn_open_select(self):
        if self.sqlconn is not None:
            self.sqlconn.close()
            self.sqlconn = None
        if self.cbbox.current() == 0:
            self.file_path = fd.askopenfilename(title="select csv file", filetypes=[("csv file", "*.csv")], initialdir=os.curdir)
        elif self.cbbox.current() == 1:
            self.file_path = fd.askopenfilename(title="select database file", filetypes=[("database file", "*.db")], initialdir=os.curdir)
        if not self.file_path:
            msgbox.showwarning('Warning', 'Failed to open file')
        self.file_path = os.path.realpath(self.file_path)
        # self.file_path = eval(repr(self.file_path).replace('/', r'\\')).lstrip(r'\?')
        self.textEntry.set('【Path】＃ '+ self.file_path )
        self.cbbox_select_changed(None)

    def getDBcolumns(self, table_name: str):
        sql = 'select * from %s limit 1' % (table_name)
        self.sqlconn._read(sql)
        col_name = [col[0] for col in self.sqlconn.cursor.description]
        return (col_name)

    def getDBrows(self, table_name: str, limit: int):
        sql = 'select * from %s' % (table_name) + ('' if limit<=0 else ' limit ' + str(limit))
        rows = self.sqlconn._read(sql)
        return (rows)

    def clearDB(self, lpr_sql: LPR_SQL):
        lpr_sql.delete_all()
        lpr_sql.init_db()

    def testDB(self, lpr_sql: LPR_SQL, size=50):
        lpr_sql.random_test(size)

    def insertCSV(self, path: str, columns: list):
        with open(file=path, mode='a+', encoding='utf_8_sig', newline='') as f:
            # writer = csv.writer(f, quoting=csv.QUOTE_ALL, delimiter=',')
            writer = csv.writer(f, delimiter=',')
            writer.writerow(columns)

    def clearCSV(self, path: str):
        column = ['lid', 'folder', 'filename', 'format', 'method', 'plate', 'color', 'predict', 'revise', 'since']
        with open(file=path, mode='w+', encoding='utf_8_sig', newline='') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(column)

    def testCSV(self, path: str, size=30):
        max_rowid = 0
        with open(file=path, mode='r', encoding='utf_8_sig') as f:
            line = f.readlines()
            if len(line)-1 == 0:
                max_rowid = 1
            else:
                max_rowid = int(line[len(line) - 1].split(',')[0])
                max_rowid+=1

        for _ in range(size):
            folder = os.path.realpath(os.path.abspath(os.curdir))
            pic_format = '.'+''.join(random.choice(['jpg','png']))
            filename = ''.join(random.sample(string.ascii_letters + string.digits, 8))
            new_filename = os.path.abspath( os.path.join(folder, filename+pic_format) )
            method = random.choice(['opencv+ocr','opencv+svm','opencv+cnn','yolo+cnn'])
            plate = (''.join(random.sample(string.ascii_letters, 2)) +'-'+ ''.join(random.sample(string.digits, 4))).upper()
            color = random.choice(['white','black','red','green','blue','yellow'])
            localtime = time.localtime()
            since = time.strftime("%Y-%m-%d %I:%M:%S", localtime)
            column = [max_rowid, folder, filename + pic_format, 'image', method, plate, color, None, None, since]
            self.insertCSV(path, column)
            max_rowid += 1

def set_center_geometry(win: tk.Tk):
    ''' 取得視窗大小和視窗位置 '''
    win.update()
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    width, height = win.winfo_width(), win.winfo_height()
    x = int((screen_width - width) / 2)
    y = int((screen_height - height) / 2)
    size = '%dx%d+%d+%d' % (width, height, x, y)
    win.geometry(size)
    win.update()

def destroy_window(event, win: tk.Tk):
    print('The window has been destroyed.')
    win.destroy()

def main():
    win = tk.Tk()
    win.geometry("1024x768")
    win.title('License Plate Recognition')
    set_center_geometry(win)
    notebook = ttk.Notebook(win)
    notebook.pack(expand=True, fill='both', side='top')
    tab3 = tk.Frame(notebook, bg='#fae3dc')
    tab3.pack(fill='both', expand=True)
    notebook.add(tab3, text=' ' * 10 + 'Report Tab' + ' ' * 10)
    t3 = TabFrame_3(tab3)
    win.protocol("WM_DELETE_WINDOW", lambda e=None, w=win:destroy_window(e, w))
    win.mainloop()

if __name__ == '__main__':
    # main()
    pass
