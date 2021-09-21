import glob
import logging
import os
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as msgbox
from tkinter import scrolledtext, ttk

import cv2
import numpy as np
from PIL import Image, ImageTk

[__all__] = ['Tab1_Frame']

class ImageProcessing:
    def __init__(self, win):
        self.__win = win
        self.img_bgr = None

    def set_imgbgr(img_bgr):
        self.img_bgr = img_bgr

    def get_imgtk(self, img_bgr, w_ratio=1/2, h_ratio=2/3):
        im = self.get_imgresize(img_bgr, w_ratio, h_ratio)
        imgtk = ImageTk.PhotoImage(image=im)
        return imgtk

    def get_imgresize(self, img_bgr, w_ratio=1/2, h_ratio=2/3):
        img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        im = Image.fromarray(img)
        height, width = im.shape[:2]
        if width > (self.__win.winfo_width()*w_ratio) or height > (self.__win.winfo_height()*h_ratio):
            width_ratio = (self.__win.winfo_width() * w_ratio) / width
            height_ratio = (self.__win.winfo_height() * h_ratio) / height
            ratio = min(width_ratio, height_ratio)
            width, height = int(width * ratio), int(height * ratio)
            width = (1 if width <= 0 else width)
            height = (1 if height <= 0 else height)
            im = im.resize((width, height), Image.ANTIALIAS)
        return im

    def thread_video(self, path):
        pass

    def thread_camera(self):
        pass

    def thread_img(self):
        pass


class Subframe1_Frame1:
    __parms = {
        'radio_btn':[
            {'text':'open image', 'col':0, 'row':0, 'sticky':'nsw', 'padx':15, 'pady':0},
            {'text':'open video', 'col':0, 'row':1, 'sticky':'nsw', 'padx':15, 'pady':0},
            {'text':'open camera', 'col':0, 'row':2, 'sticky':'nsw', 'padx':15, 'pady':0},
            {'text':'connect app', 'col':0, 'row':3, 'sticky':'nsw', 'padx':15, 'pady':0}
        ]
    } # yapf: disable

    def __init__(self, iframe_sub, command=None):
        self.__frame = iframe_sub[0][0]
        self.radiobtn_val = tk.IntVar()
        self.__btn = [ None for _ in self.__parms['radio_btn'] ]

        for idx, _ in enumerate(self.__btn):
            abbr = self.__parms['radio_btn'][idx]
            text = abbr['text']
            font = ('microsoft yahei', 10, 'bold underline')
            self.__btn[idx] = tk.Radiobutton(master=self.__frame, text=text, value=idx, variable=self.radiobtn_val, font=font, command=command) # yapf: disable
            col, row, sticky, padx, pady = abbr['col'], abbr['row'], abbr['sticky'], abbr['padx'], abbr['pady'] # yapf: disable
            self.__btn[idx].grid(column=col, row=row, sticky=sticky, padx=padx, pady=pady) # yapf: disable
        self.radiobtn_val.set(0)

class Subframe1_Frame2:
    __parms = {
        'combobox': {'values':['open files', 'open folder'], 'state':'readonly', 'col':0, 'row':0, 'sticky':'nsew', 'padx':10, 'pady':10},
        'button': {'width':18, 'height':18, 'borderwidth':1, 'col':1, 'row':0, 'sticky':'nsew', 'padx':10, 'pady':10},
        'icon' : ['files-623003.ico', 'folder_72px.png']
    } # yapf: disable

    def __init__(self, iframe_sub):
        self.__frame = iframe_sub[0][1]
        self.icon = self.__parms['icon']

        abbr = self.__parms['combobox']
        self.cbbox = ttk.Combobox(master=self.__frame, values=abbr['values'], state=abbr['state']) # yapf:disable
        self.cbbox.grid(column=abbr['col'], row=abbr['row'], sticky=abbr['sticky'], padx=abbr['padx'], pady=abbr['pady']) # yapf:disable
        self.cbbox.current(0)

        abbr, imgtk = self.__parms['button'], self.__get_imgtk(img_icon=self.icon[0], size=(20,20))  # yapf:disable
        self.btn = tk.Button(master=self.__frame, image=imgtk, width=abbr['width'], height=abbr['height'], borderwidth=abbr['borderwidth']) # yapf:disable
        self.btn.grid(column=abbr['col'], row=abbr['row'], sticky=abbr['sticky'], padx=abbr['padx'], pady=abbr['pady']) # yapf:disable
        self.btn.image = imgtk

    def __get_imgtk(self, img_icon, size=(20,20)):
        img_path = os.path.join(os.curdir, 'icon', img_icon)
        img = Image.open(img_path).resize(size, Image.ANTIALIAS)
        imgtk = ImageTk.PhotoImage(img)
        return imgtk

class Subframe1_Frame3:
    __parms = {
        'entry': {'col':0, 'row':0, 'sticky':'nsew', 'padx':10, 'pady':10, 'width':22},
        'label': {'col':1, 'row':0, 'sticky':'nsew', 'padx':10, 'pady':10},
        'icon' : ['close_72px.png', 'refresh_72px.png']
    } # yapf: disable

    def __init__(self, iframe_sub):
        self.__frame = iframe_sub[0][2]
        self.icon = self.__parms['icon']

        abbr = self.__parms['entry']
        self.entry_val = tk.StringVar()
        self.entry = ttk.Entry(master=self.__frame, textvariable=self.entry_val, width=abbr['width']) # yapf:disable
        self.entry.grid(column=abbr['col'], row=abbr['row'], sticky=abbr['sticky'], padx=abbr['padx'], pady=abbr['pady']) # yapf:disable
        self.entry_val.set('0.0.0.0')

        abbr, imgtk = self.__parms['label'], self.__get_imgtk(img_icon=self.icon[0], size=(20,20))  # yapf:disable
        self.label = ttk.Label(master=self.__frame, image=imgtk) # yapf:disable
        self.label.grid(column=abbr['col'], row=abbr['row'], sticky=abbr['sticky'], padx=abbr['padx'], pady=abbr['pady']) # yapf:disable
        self.label.image = imgtk

    def __get_imgtk(self, img_icon, size=(20, 20)):
        img_path = os.path.join(os.curdir, 'icon', img_icon)
        img = Image.open(img_path).resize(size, Image.ANTIALIAS)
        imgtk = ImageTk.PhotoImage(img)
        return imgtk

class Subframe2_Frame1:
    __parms =  {
        'empty_frame':[
            {'col':0, 'row':0, 'sticky':'nsew'},
            {'col':0, 'row':1, 'sticky':'nsew'}
        ],
        'combobox_title':{'text':'choose one of the methods to recognize :','col':0, 'row':0, 'sticky':'nsew', 'padx':10, 'pady':0, 'justify':'left'},
        'combobox':{'values':['opencv + ocr', 'opencv + svm', 'opencv + cnn', 'yolo + cnn'], 'state':'readonly',
                    'col':1, 'row':0, 'sticky':'nsew', 'padx':10, 'pady':5},
        'folder_title':{'text':'【 Folder Path 】 : ','col':0, 'row':1, 'sticky':'nsw', 'padx':10, 'pady':0, 'anchor':'center'},
        'folder_content':{'text':'','col':1, 'row':1, 'sticky':'nsew', 'padx':10, 'pady':0,'relief':'groove', 'bg':'white', 'anchor':'w'},
        'file_title':{'text':'【 FileName 】 : ','col':0, 'row':2, 'sticky':'nsw', 'padx':10, 'pady':5, 'anchor':'center'},
        'file_content':{'text':'','col':1, 'row':2, 'sticky':'nsew', 'padx':10, 'pady':5, 'relief':'groove', 'bg':'white', 'anchor':'w'},
    } # yapf:disable

    def __init__(self, iframe_sub):
        self.__frame = iframe_sub[1][0]
        emptyframe = [None for _ in self.__parms['empty_frame']]
        for idx, _ in enumerate(emptyframe):
            abbr = self.__parms['empty_frame'][idx]
            emptyframe[idx] = tk.Frame(master=self.__frame)
            emptyframe[idx].grid(column=abbr['col'], row=abbr['row'], sticky=abbr['sticky'])

        abbr = self.__parms['combobox_title']
        self.cbbox_title = tk.Label(master=emptyframe[0], text=abbr['text'], justify =abbr['justify']) # yapf:disable
        self.cbbox_title.grid(column=abbr['col'], row=abbr['row'], sticky=abbr['sticky'], padx=abbr['padx'], pady=abbr['pady']) # yapf:disable

        abbr = self.__parms['combobox']
        self.combobox = ttk.Combobox(master=emptyframe[0], values=abbr['values'], state=abbr['state']) # yapf:disable
        self.combobox.grid(column=abbr['col'], row=abbr['row'], sticky=abbr['sticky'], padx=abbr['padx'], pady=abbr['pady']) # yapf:disable
        self.combobox.current(0)

        abbr = self.__parms['folder_title']
        self.folder_title = tk.Label(master=emptyframe[1], text=abbr['text'], anchor=abbr['anchor']) # yapf:disable
        self.folder_title.grid(column=abbr['col'], row=abbr['row'], sticky=abbr['sticky'], padx=abbr['padx'], pady=abbr['pady']) # yapf:disable

        abbr = self.__parms['folder_content']
        self.folder_content = tk.Label(master=emptyframe[1], text=abbr['text'], relief=abbr['relief'], background=abbr['bg'], anchor=abbr['anchor']) # yapf:disable
        self.folder_content.grid(column=abbr['col'], row=abbr['row'], sticky=abbr['sticky'], padx=abbr['padx'], pady=abbr['pady']) # yapf:disable

        abbr = self.__parms['file_title']
        self.file_title = tk.Label(master=emptyframe[1], text=abbr['text'], anchor=abbr['anchor']) # yapf:disable
        self.file_title.grid(column=abbr['col'], row=abbr['row'], sticky=abbr['sticky'], padx=abbr['padx'], pady=abbr['pady']) # yapf:disable

        abbr = self.__parms['file_content']
        self.file_content = tk.Label(master=emptyframe[1], text=abbr['text'], relief=abbr['relief'], background=abbr['bg'], anchor=abbr['anchor']) # yapf:disable
        self.file_content.grid(column=abbr['col'], row=abbr['row'], sticky=abbr['sticky'], padx=abbr['padx'], pady=abbr['pady']) # yapf:disable

        emptyframe[1].columnconfigure(0, weight=0)
        emptyframe[1].columnconfigure(1, weight=1)

class Subframe2_Frame2:
    __parms = {
        'button_1':{'text':'◀','col':0, 'row':0, 'sticky':'w', 'padx':0, 'pady':0, 'width':20, 'height':20, 'compound':'c', 'borderwidth':1, 'background':'white'},
        'canvas':{'text':'','col':1, 'row':0, 'sticky':'nsew', 'padx':0, 'pady':0},
        'button_2':{'text':'▶','col':2, 'row':0, 'sticky':'w', 'padx':0, 'pady':0, 'width':20, 'height':20, 'compound':'c', 'borderwidth':1, 'background':'white'},
    } # yapf:disable

    def __init__(self, iframe_sub):
        self.__frame = iframe_sub[1][1]
        self.__virtual_img = tk.PhotoImage(width=1, height=1)

        abbr = self.__parms['button_1']
        self.btn_left = tk.Button(master=self.__frame, text=abbr['text'], image=self.__virtual_img, width=abbr['width'], height=abbr['height'],
                                  compound=abbr['compound'], borderwidth=abbr['borderwidth'], background=abbr['background']) # yapf:disable
        self.btn_left.grid(column=abbr['col'], row=abbr['row'], sticky=abbr['sticky']) # yapf:disable

        abbr = self.__parms['canvas']
        self.canvas = tk.Canvas(master=self.__frame)
        self.canvas.create_image(0,0, anchor='center', image=self.__virtual_img, tags="bg_img") # yapf:disable
        self.canvas.grid(column=abbr['col'], row=abbr['row'], sticky=abbr['sticky']) # yapf:disable

        abbr = self.__parms['button_2']
        self.btn_right = tk.Button(master=self.__frame, text=abbr['text'], image=self.__virtual_img, width=abbr['width'], height=abbr['height'],
                                  compound=abbr['compound'], borderwidth=abbr['borderwidth'], background=abbr['background']) # yapf:disable
        self.btn_right.grid(column=abbr['col'], row=abbr['row'], sticky=abbr['sticky']) # yapf:disable



class Subframe2_Frame3:
    __parms = {
        'button_1':{'text':'▶','col':0, 'row':0, 'sticky':'nsew', 'padx':5, 'pady':0, 'width':50, 'height':50, 'compound':'c', 'borderwidth':1, 'background':'white'},
        'button_2':{'text':'▌▌','col':1, 'row':0, 'sticky':'nsew', 'padx':5, 'pady':0, 'width':50, 'height':50, 'compound':'c', 'borderwidth':1, 'background':'white'},
        'button_3':{'text':'▅','col':2, 'row':0, 'sticky':'nsew', 'padx':5, 'pady':0, 'width':50, 'height':50, 'compound':'c', 'borderwidth':1, 'background':'white'},
        'button_4':{'text':'Rec','col':3, 'row':0, 'sticky':'nsew', 'padx':5, 'pady':0, 'width':50, 'height':50, 'compound':'c', 'borderwidth':1, 'background':'white'},
    } # yapf:disable

    def __init__(self, iframe_sub):
        self.__frame = iframe_sub[1][2]
        self.__virtual_img = tk.PhotoImage(width=1, height=1)
        self.__frame.columnconfigure([0,1,2,3], weight=1)

        abbr = self.__parms['button_1']
        self.btn_1 = tk.Button(master=self.__frame, text=abbr['text'], image=self.__virtual_img, width=abbr['width'], height=abbr['height'],
                                  compound=abbr['compound'], borderwidth=abbr['borderwidth'], background=abbr['background']) # yapf:disable
        self.btn_1.grid(column=abbr['col'], row=abbr['row'], sticky=abbr['sticky']) # yapf:disable

        abbr = self.__parms['button_2']
        self.btn_2 = tk.Button(master=self.__frame, text=abbr['text'], image=self.__virtual_img, width=abbr['width'], height=abbr['height'],
                                  compound=abbr['compound'], borderwidth=abbr['borderwidth'], background=abbr['background']) # yapf:disable
        self.btn_2.grid(column=abbr['col'], row=abbr['row'], sticky=abbr['sticky']) # yapf:disable

        abbr = self.__parms['button_3']
        self.btn_3 = tk.Button(master=self.__frame, text=abbr['text'], image=self.__virtual_img, width=abbr['width'], height=abbr['height'],
                                  compound=abbr['compound'], borderwidth=abbr['borderwidth'], background=abbr['background']) # yapf:disable
        self.btn_3.grid(column=abbr['col'], row=abbr['row'], sticky=abbr['sticky']) # yapf:disable

        abbr = self.__parms['button_4']
        self.btn_4 = tk.Button(master=self.__frame, text=abbr['text'], image=self.__virtual_img, width=abbr['width'], height=abbr['height'],
                                  compound=abbr['compound'], borderwidth=abbr['borderwidth'], background=abbr['background']) # yapf:disable
        self.btn_4.grid(column=abbr['col'], row=abbr['row'], sticky=abbr['sticky']) # yapf:disable


class Tab1_Frame:
    __parms = [
            {
                'mainframe':
                    {'text':'Image Source', 'col':0, 'row':0, 'sticky':'nsew', 'padx':5, 'pady':5, 'colspan':1 ,'rowspan':1},
                'subframe':[
                    {'text':'Click one of the models :', 'col':0, 'row':0, 'sticky':'nsew', 'padx':10, 'pady':10, 'colspan':1 ,'rowspan':2},
                    {'text':'Click one of the options :', 'col':1, 'row':0, 'sticky':'nsew', 'padx':10, 'pady':10, 'colspan':1 ,'rowspan':1},
                    {'text':'Entry ip from the ip camera :', 'col':1, 'row':1, 'sticky':' nsew', 'padx':10, 'pady':10, 'colspan':1 ,'rowspan':1}
                ]
            },{
                'mainframe':
                    {'text':'Image Display', 'col':0, 'row':1, 'sticky':'nsew', 'padx':5, 'pady':5, 'colspan':1 ,'rowspan':1},
                'subframe':[
                    {'text':'', 'col':0, 'row':0, 'sticky':'nsew', 'padx':10, 'pady':5, 'colspan':1 ,'rowspan':1},
                    {'text':'', 'col':0, 'row':1, 'sticky':'nsew', 'padx':10, 'pady':5, 'colspan':1 ,'rowspan':1},
                    {'text':'', 'col':0, 'row':2, 'sticky':'nsew', 'padx':10, 'pady':5, 'colspan':1 ,'rowspan':1}
                ]
            },{
                'mainframe':
                    {'text':'Image Analysis', 'col':1, 'row':0, 'sticky':'nsew', 'padx':5, 'pady':5, 'colspan':1 ,'rowspan':2},
                'subframe':[
                    {'text':'license plate position predict: ', 'col':0, 'row':0, 'sticky':'nsew', 'padx':10, 'pady':10, 'colspan':1 ,'rowspan':1},
                    {'text':'license plate characters predict: ', 'col':0, 'row':1, 'sticky':'nsew', 'padx':10, 'pady':10, 'colspan':1 ,'rowspan':1},
                    {'text':'license plate color predict: ', 'col':0, 'row':2, 'sticky':'nsew', 'nsew':10, 'padx':10, 'pady':10, 'colspan':1 ,'rowspan':1},
                    {'text':'license plate text predict: ', 'col':0, 'row':3, 'sticky':'nsew', 'nsew':10, 'padx':10, 'pady':10, 'colspan':1 ,'rowspan':1},
                    {'text':'license plate infomation Submit', 'col':0, 'row':4, 'sticky':'nsew', 'padx':10, 'pady':10, 'colspan':1 ,'rowspan':1}
                ]
            }] # yapf:disable

    def __init__(self, win, TabFrame):
        self.win = win
        self.__tab1 = TabFrame
        self.files, self.files_idx = [], 0
        self.file_path, self.folder_name, self.file_name = '', '', ''
        self.__iframe = [ None for _ in self.__parms ]
        self.__iframe_sub = [ [ None for _ in parm['subframe'] ] for parm in self.__parms ]
        self.canvas_frame = None


        #【Tab1_Frame.labelframe1, Tab1_Frame.labelframe2, Tab1_Frame.labelframe3】
        for idx, _ in enumerate(self.__iframe):
            abbr = self.__parms[idx]['mainframe']
            text = abbr['text']
            self.__iframe[idx] = tk.LabelFrame(master=self.__tab1, text=text)
            col, row, sticky  = abbr['col'], abbr['row'], abbr['sticky']
            padx, pady, colspan, rowspan = abbr['padx'], abbr['pady'], abbr['colspan'], abbr['rowspan']
            self.__iframe[idx].grid(column=col, row=row, sticky=sticky, padx=padx, pady=pady, columnspan=colspan, rowspan=rowspan) # yapf:disable

        for idx, _ in enumerate(self.__iframe_sub):
            for idy, abbr in enumerate(self.__parms[idx]['subframe']):
                text = abbr['text']
                self.__iframe_sub[idx][idy] = tk.LabelFrame(master=self.__iframe[idx], text=text) # yapf:disable
                col, row, sticky  = abbr['col'], abbr['row'], abbr['sticky']
                padx, pady, colspan, rowspan = abbr['padx'], abbr['pady'], abbr['colspan'], abbr['rowspan']
                self.__iframe_sub[idx][idy].grid(column=col, row=row, sticky=sticky, padx=padx, pady=pady, columnspan=colspan, rowspan=rowspan) # yapf:disable

        # iframe, iframe_sub 切版
        self.__tab1.columnconfigure([0], weight=0)
        self.__tab1.columnconfigure([1], weight=1)
        self.__tab1.rowconfigure([0], weight=0)
        self.__tab1.rowconfigure([1], weight=1)

        self.__iframe[0].columnconfigure(0, weight=1)
        self.__iframe[0].columnconfigure(1, weight=9)
        self.__iframe[0].rowconfigure([0,1], weight=0)
        self.__iframe[1].columnconfigure(0,weight=1)
        self.__iframe[1].rowconfigure([0,2], weight=0)
        self.__iframe[1].rowconfigure(1, weight=5)
        self.__iframe[2].columnconfigure(0, weight=1)
        self.__iframe[2].rowconfigure([0,1], weight=1)
        self.__iframe[2].rowconfigure([2,3,4], weight=1)

        self.__iframe_sub[1][0].columnconfigure([0], weight=1)
        self.__iframe_sub[1][0].rowconfigure([0,1,2], weight=0)
        self.__iframe_sub[1][1].columnconfigure([0,2], weight=0)
        self.__iframe_sub[1][1].columnconfigure([1], weight=1)
        self.__iframe_sub[1][1].rowconfigure([0], weight=1)

        self.i_1 = Subframe1_Frame1(self.__iframe_sub)
        self.i_2 = Subframe1_Frame2(self.__iframe_sub)
        self.i_3 = Subframe1_Frame3(self.__iframe_sub)

        self.j_1 = Subframe2_Frame1(self.__iframe_sub)
        self.j_2 = Subframe2_Frame2(self.__iframe_sub)
        self.j_3 = Subframe2_Frame3(self.__iframe_sub)

    # def cbbox_select_changed(self, event):
    #     img_name, imgtk = '', None
    #     if self.__radio_val == 0:
    #         img_name = os.path.join(os.curdir, 'icon', self.__parms['icon'][0])
    #         imgtk = self.__get_imgtk_icon(img_path=img_name, size=(20, 20))
    #     elif self.__radio_val == 1:
    #         img_name = os.path.join(os.curdir, 'icon', self.__parms['icon'][1])
    #         imgtk = self.__get_imgtk_icon(img_path=img_name, size=(20, 20))
    #     self.btn.image = imgtk
    #     self.btn.config(image=imgtk)

    # def btn_open(self):
    #     title = ['select image files', 'select video files', 'select image directory', 'select video directory']
    #     filetypes = [[("image file", "*.jpg"),("image file", "*.png"),("image file", "*.gif")],
    #                  [("video file", "*.mov"),("video file", "*.ts"),("video file", "*.avi"),("video file", "*.mpeg"),("video file", "*.mp4")]]
    #     initialdir = os.curdir
    #     file_extend = [('*.jpg', '*.png', '*.gif'), ('*.mov','*.ts','*.avi','*.mpeg','*.mp4')]
    #     if self.cbbox.current() == 0:
    #         if self.__radio_val.get() == 0:
    #             self.files = fd.askopenfilenames(title=title[0], filetypes=filetypes[0], initialdir=initialdir)
    #         elif self.__radio_val.get() == 1:
    #             self.files = fd.askopenfilenames(title=title[1], filetypes=filetypes[1], initialdir=initialdir)
    #     elif self.cbbox.current() == 1:
    #         if self.__radio_val.get() == 0:
    #             self.folder_path = fd.askdirectory(title=title[2], initialdir=initialdir)
    #             [ self.files.extend(glob.glob( os.path.abspath(os.path.join(self.folder_path, ext)))) for ext in file_extend[0] ]
    #         elif self.__radio_val.get() == 1:
    #             self.folder_path = fd.askdirectory(title=title[3], initialdir=initialdir)
    #             [ self.files.extend(glob.glob( os.path.abspath(os.path.join(self.folder_path, ext)))) for ext in file_extend[1] ]
    #     self.file_path = os.path.abspath(self.files[self.files_idx])
    #     self.folder_name = os.path.dirname(self.file_path)
    #     self.file_name = os.path.basename(self.file_path)

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
    tab1 = tk.Frame(notebook, bg='#fae3dc')
    tab1.pack(fill='both', expand=True)
    notebook.add(tab1, text=' ' * 10 + 'Demo Tab' + ' ' * 10)
    t1 = Tab1_Frame(win, tab1)
    win.protocol("WM_DELETE_WINDOW", lambda e=None, w=win:destroy_window(e, w))
    win.mainloop()

if __name__ == '__main__':
    main()
    pass
