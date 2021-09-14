import csv
import os
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as msgbox
from tkinter import scrolledtext, ttk

import cv2
from PIL import Image, ImageTk

try:
    from lib.sqlite2crud import sqlite2CRUD as sqlcrud
except:
    from sqlite2crud import sqlite2CRUD as sqlcrud

class scrolledTreeview(tk.Frame):
    def __init__(self, parent=None, style=None, x=0, y=0,*args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.style = style
        self.x = x
        self.y = y
        self.parent.columnconfigure(self.x, weight=1)
        self.parent.rowconfigure(self.y, weight=1)
        self.treeview = ttk.Treeview(self.parent, style="Custom.Treeview")
        # self.treeview = ttk.Treeview(self.parent)
        self.treeview.grid(column=self.x, row=self.y, sticky='nsew', columnspan=2)

        self.xscrbar = ttk.Scrollbar(self.parent, orient='horizontal')
        self.xscrbar.grid(column=self.x, row=self.y+1, sticky='swe')
        self.yscrbar = ttk.Scrollbar(self.parent, orient='vertical')
        self.yscrbar.grid(column=self.x+1, row=self.y, sticky='nse')

        self.xscrbar.config(command=self.treeview.xview)
        self.yscrbar.config(command=self.treeview.yview)
        self.treeview.configure(xscrollcommand=self.xscrbar.set, yscrollcommand=self.yscrbar.set)

    def CSV2Treeview(self, col_name, col_name_display, rows):
        self.treeview.configure(columns=col_name, show='headings')

        # 設置列寬度
        for _, col in enumerate(col_name):
            self.treeview.column(col, minwidth=50, width=100, stretch=True, anchor='n')
        # 添加列名稱顯示
        if len(col_name_display) == len(col_name):
            for idx, col in enumerate(col_name_display):
                self.treeview.heading(col_name[idx], text=col)
        else:
            print('col_name array size != col_name_display array size')
            return
        # 添加表格數據
        for _, row in enumerate(rows):
            temp = [str(row[0]).zfill(10)] + row[1:]
            self.treeview.insert('', 'end', values=temp, tag='gray')
        self.treeview.tag_configure('gray', background='#cccccc')

        for col in col_name:
            self.treeview.heading(col, text=col, command=lambda _col=col: self.sort_column(_col, False))

    def sql2Treeview(self, col_name, col_name_display, rows):
        self.treeview.configure(columns=col_name, show='headings')

        # 設置列寬度
        for _, col in enumerate(col_name):
            self.treeview.column(col, minwidth=100, width=50, stretch=True, anchor='n')
        # 添加列名稱顯示
        if len(col_name_display) == len(col_name):
            for idx, col in enumerate(col_name_display):
                self.treeview.heading(col_name[idx], text=col)
        else:
            print('col_name array size != col_name_display array size')
            return
        # 添加表格數據
        for _, row in enumerate(rows):
            temp = (*(), str(row[0]).zfill(10)) + row[1:]
            self.treeview.insert('', 'end', values=temp, tag='gray')
        self.treeview.tag_configure('gray', background='#cccccc')

        for col in col_name:
            self.treeview.heading(col, text=col, command=lambda _col=col: self.sort_column(_col, False))

    def getsqlcolumns(self, sqlconn, table_name:str):
        sql = 'select * from %s limit 1' % (table_name)
        sqlconn._read(sql)
        col_name = [col[0] for col in sqlconn.cursor.description]
        return (col_name)

    def getsqlrows(self, sqlconn: sqlcrud, table_name:str, limit: int):
        sql = 'select * from %s' % (table_name) + ' limit ' + str(limit)
        rows = sqlconn._read(sql)
        return (rows)

    def csv2Treeview(self, csv):
        pass

    def sort_column(self, column, reverse):
        l = [(self.treeview.set(k, column), k) for k in self.treeview.get_children('')]
        # print(self.treeview.get_children(''))
        l.sort(reverse=reverse)#排序方式
        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):#根據排序後索引移動
            self.treeview.move(k, '', index)
            # print(k)
        self.treeview.heading(column, command=lambda: self.sort_column(column, not reverse))#重寫標題，使之成為再點倒序的標題

class tab3(tk.Frame):
    def __init__(self, tab_3):
        super(tab3, self).__init__(tab_3)
        self.tab_3 = tab_3
        self.file_path = ''

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
        self.style.configure("Custom.Treeview.Heading",
            background="blue", foreground="white", relief="flat")
        self.style.map("Custom.Treeview.Heading",
            relief=[('active','groove'),('pressed','sunken')])

        frame = tk.Frame(master=self.tab_3)
        frame.grid(column=0, row=0, sticky='nsew', pady=5, columnspan=2)

        self.cbbox = ttk.Combobox(master=frame, values=['report csv','report sql'], state='readonly')
        self.cbbox.current(1)
        self.cbbox.pack(anchor='n', side='left', fill='both')
        self.img = Image.open(os.path.join(os.curdir,'icon','folder-home-open.png')).resize((20,20),Image.ANTIALIAS)
        self.imgtk = ImageTk.PhotoImage(self.img)
        self.btn = tk.Button(master=frame, image=self.imgtk, width=20, height=20, borderwidth=2)
        self.btn.config(command=(lambda:self.csv_sql_open()))
        self.btn.pack(anchor='n', side='left', padx=20, fill='both')

        self.textEntry = tk.StringVar()
        self.entry = tk.Entry(master=frame, textvariable=self.textEntry)
        self.entry.pack(anchor='n', side='left', expand=True,fill='both')
        self.cbbox.bind('<<ComboboxSelected>>', (lambda e=None: self.cbbox_select_changed(e)) )
        self.cbbox_select_changed(None)

    def cbbox_select_changed(self, event):
        self.treeview = None
        if self.cbbox.current() == 0:
            self.treeview = scrolledTreeview(parent=self.tab_3, style=self.style, x=0, y=1)
            if not (os.path.exists(self.file_path) and self.file_path.find('.csv') > 0):
                self.file_path = os.path.join(os.path.abspath(os.path.curdir),'source','example.csv')
            with open(file=self.file_path, mode='r', encoding='utf_8_sig') as f:
                reader = csv.reader(f)
                tree_column = [i.strip() for i in next(reader)]
                # print(tree_column)
                tree_column_display = ['流水號', '檔名', '辨識方式', '辨識結果', '顏色', '正確判斷', '辨識時間' ]
                tree_rows = [[x.strip() for x in row] for row in reader]
                # for row in tree_rows:
                #     print(row)
                self.treeview.CSV2Treeview(tree_column, tree_column_display, tree_rows)
        elif self.cbbox.current() == 1:
            self.treeview = scrolledTreeview(parent=self.tab_3, style=self.style, x=0, y=1)
            if not (os.path.exists(self.file_path) and self.file_path.find('.db') > 0):
                self.file_path = os.path.join(os.path.abspath(os.path.curdir),'source','example.db')
            sqlconn = sqlcrud(self.file_path)
            tree_column = self.treeview.getsqlcolumns(sqlconn, 'LPR')
            # print(tree_column)
            tree_column_display = ['流水號', '檔名', '辨識方式', '辨識結果', '顏色', '正確判斷', '辨識時間' ]
            tree_rows = self.treeview.getsqlrows(sqlconn, 'LPR', 100)
            # for row in tree_rows:
            #     print(row)
            self.treeview.sql2Treeview(tree_column, tree_column_display, tree_rows)
            sqlconn.close()
        self.file_path = os.path.realpath(self.file_path)
        # self.file_path = eval(repr(self.file_path).replace('/', r'\\')).lstrip(r'\?')
        self.textEntry.set('[path]: ' + self.file_path)

    def csv_sql_open(self):
        if self.cbbox.current() == 0:
            self.file_path = fd.askopenfilename(title="select csv file", filetypes=[("csv file", "*.csv")], initialdir=os.curdir)
        elif self.cbbox.current() == 1:
            self.file_path = fd.askopenfilename(title="select database file", filetypes=[("database file", "*.db")], initialdir=os.curdir)
        if not self.file_path:
            msgbox.showwarning('Warning', 'Failed to open file')
        self.file_path = os.path.realpath(self.file_path)
        # self.file_path = eval(repr(self.file_path).replace('/', r'\\')).lstrip(r'\?')
        self.textEntry.set('[path]: '+ self.file_path )
        self.cbbox_select_changed(None)

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


def main():
    win = tk.Tk()
    win.geometry("1024x768")
    win.title('License Plate Recognition')
    set_center_geometry(win)
    notebook = ttk.Notebook(win)
    notebook.pack(expand=True, fill='both', side='top')
    tab_3 = tk.Frame(notebook, bg='#fae3dc')
    tab_3.pack(fill='both', expand=True)
    notebook.add(tab_3, text=' ' * 10 + 'Report Tab' + ' ' * 10)
    t3 = tab3(tab_3)
    win.mainloop()

if __name__ == '__main__':
    # main()
    pass
