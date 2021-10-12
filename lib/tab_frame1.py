import glob
import logging
import os
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as msgbox
from tkinter import scrolledtext, ttk

import cv2
from PIL import Image, ImageTk


class scrolledWidget(tk.Frame):
    def __init__(self, parent, widget, x=0, y=0,*args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.x = x
        self.y = y
        self.parent.columnconfigure(self.x, weight=1)
        self.parent.rowconfigure(self.y, weight=1)
        self.__widget = widget(self.parent)
        self.__widget.grid(column=self.x, row=self.y, sticky='nsew', columnspan=2)

        self.__xscrbar = ttk.Scrollbar(self.parent, orient='horizontal')
        self.__xscrbar.grid(column=self.x, row=self.y+1, sticky='swe')
        self.__yscrbar = ttk.Scrollbar(self.parent, orient='vertical')
        self.__yscrbar.grid(column=self.x+1, row=self.y, sticky='nse')

        self.__xscrbar.config(command=self.__widget.xview)
        self.__yscrbar.config(command=self.__widget.yview)
        self.__widget.configure(xscrollcommand=self.__xscrbar.set, yscrollcommand=self.__yscrbar.set)

class ImageProcessing:
    def __init__(self):
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
        height, width = img.shape[:2]
        if width > (self.win.winfo_width()*w_ratio) or height > (self.win.winfo_height()*h_ratio):
            width_ratio = (self.win.winfo_width()/2) / width
            height_ratio = (self.win.winfo_height()*2/3) / height
            ratio = min(width_ratio, height_ratio)

            width, height = int(width*ratio), int(height*ratio)
            width = ( 1 if width<=0 else width )
            height = ( 1 if height<=0 else height )
            im = im.resize((width, height), Image.ANTIALIAS)
        return im

    def thread_video(self, path):
        pass

    def thread_camera(self):
        pass

    def thread_img(self):
        pass

class Subframe1_Frame1:
    def __init__(self):
        pass

class TabFrame_1(tk.Frame):
    def __init__(self, win, tab1):
        super(TabFrame_1, self).__init__(win, tab1)
        self.win = win
        self.tab1 = tab1
        self.files, self.files_idx = [], 0
        self.file_path, self.folder_name, self.file_name = '', '', ''
        self.tab1.columnconfigure([0], weight=1)
        self.tab1.columnconfigure([1], weight=2)
        self.tab1.rowconfigure([0], weight=0)
        self.tab1.rowconfigure([1], weight=5)

        self.parms = [
            {
                'mainframe':
                    {'text':'Image Source', 'col':0, 'row':0, 'sticky':'nsew', 'padx':5, 'pady':5, 'colspan':1 ,'rowspan':1},
                'subframe':[
                    {'text':'Click one of the models :', 'col':0, 'row':0, 'sticky':'nsew', 'padx':10, 'pady':10, 'colspan':1 ,'rowspan':2},
                    {'text':'Click one of the options :', 'col':1, 'row':0, 'sticky':'new', 'padx':10, 'pady':10, 'colspan':1 ,'rowspan':1},
                    {'text':'Entry ip from the ip camera :', 'col':1, 'row':1, 'sticky':' sew', 'padx':10, 'pady':10, 'colspan':1 ,'rowspan':1}
                ],
                'radiobutton':[
                    {'text':'open image', 'col':0, 'row':0, 'sticky':'nsw', 'padx':15, 'pady':0},
                    {'text':'open video', 'col':0, 'row':1, 'sticky':'nsw', 'padx':15, 'pady':0},
                    {'text':'open camera', 'col':0, 'row':2, 'sticky':'nsw', 'padx':15, 'pady':0},
                    {'text':'connect app', 'col':0, 'row':3, 'sticky':'nsw', 'padx':15, 'pady':0}
                ],
                'combobox': {'values':['open single/multiple files', 'open folder'], 'state':'readonly', 'col':0, 'row':0, 'sticky':'nsew', 'padx':10, 'pady':10},
                'button': {'width':18, 'height':18, 'borderwidth':1, 'col':1, 'row':0, 'sticky':'nsew', 'padx':10, 'pady':10},
                'entry': {'col':0, 'row':0, 'sticky':'nsew', 'padx':10, 'pady':10, 'width':22},
                'label': {'col':1, 'row':0, 'sticky':'nsew', 'padx':10, 'pady':10},
            },
            {
                'mainframe':
                    {'text':'Image Display', 'col':0, 'row':1, 'sticky':'nsew', 'padx':5, 'pady':5, 'colspan':1 ,'rowspan':1},
                'subframe':[
                    {'text':'', 'col':0, 'row':0, 'sticky':'nsew', 'padx':10, 'pady':5, 'colspan':1 ,'rowspan':1},
                    {'text':'', 'col':0, 'row':1, 'sticky':'nsew', 'padx':10, 'pady':5, 'colspan':1 ,'rowspan':1}
                ],
                'label_1':{'text':'choose one of the\n methods to recognize :','col':0, 'row':0, 'sticky':'nsw', 'padx':10, 'pady':0, 'justify':'left'},
                'combobox':{'values':['opencv + ocr', 'opencv + svm', 'opencv + cnn', 'yolo + cnn'], 'state':'readonly', 'col':1, 'row':0, 'sticky':'nsew', 'padx':10, 'pady':5},
                'label_2':{'text':'【 Folder Path 】 : ','col':0, 'row':1, 'sticky':'nsw', 'padx':10, 'pady':0, 'anchor':'center'},
                'label_3':{'text':'','col':1, 'row':1, 'sticky':'nsew', 'padx':10, 'pady':0,'relief':'groove', 'bg':'white', 'anchor':'w'},
                'label_4':{'text':'【 FileName Path 】 : ','col':0, 'row':2, 'sticky':'nsw', 'padx':10, 'pady':5, 'anchor':'center'},
                'label_5':{'text':'','col':1, 'row':2, 'sticky':'nsew', 'padx':10, 'pady':5, 'relief':'groove', 'bg':'white', 'anchor':'w'},
                'button_1':{'text':'◀','col':0, 'row':0, 'sticky':'w', 'padx':0, 'pady':0, 'width':20, 'height':20, 'compound':'c', 'borderwidth':1, 'background':'white'},
                'canvas':{'text':'','col':1, 'row':0, 'sticky':'nsew', 'padx':0, 'pady':0},
                'button_2':{'text':'▶','col':2, 'row':0, 'sticky':'w', 'padx':0, 'pady':0, 'width':20, 'height':20, 'compound':'c', 'borderwidth':1, 'background':'white'},

            },
            {
                'mainframe':
                    {'text':'Image Analysis', 'col':1, 'row':0, 'sticky':'nsew', 'padx':5, 'pady':5, 'colspan':1 ,'rowspan':2},
                'subframe':[
                    {'text':'license plate position predict: ', 'col':0, 'row':0, 'sticky':'nsew', 'padx':10, 'pady':10, 'colspan':1 ,'rowspan':1},
                    {'text':'license plate characters predict: ', 'col':0, 'row':1, 'sticky':'nsew', 'padx':10, 'pady':10, 'colspan':1 ,'rowspan':1},
                    {'text':'license plate color predict: ', 'col':0, 'row':2, 'sticky':'nsew', 'nsew':10, 'padx':10, 'pady':10, 'colspan':1 ,'rowspan':1},
                    {'text':'license plate text predict: ', 'col':0, 'row':3, 'sticky':'nsew', 'nsew':10, 'padx':10, 'pady':10, 'colspan':1 ,'rowspan':1},
                    {'text':'', 'col':0, 'row':4, 'sticky':'nsew', 'padx':10, 'pady':10, 'colspan':1 ,'rowspan':1}
                ]
            }
        ] # yapf:disable
        parms = self.parms
        #【TabFrame_1.labelframe1, TabFrame_1.labelframe2, TabFrame_1.labelframe3】
        self.iframe = []
        for idx, parm in enumerate(parms):
            text = parm['mainframe']['text']
            self.iframe.append(tk.LabelFrame(master=self.tab1, text=text)) # yapf:disable
        for idx, iframe in enumerate(self.iframe):
            abbr = parms[idx]['mainframe']
            col, row, sticky  = abbr['col'], abbr['row'], abbr['sticky']
            padx, pady, colspan, rowspan = abbr['padx'], abbr['pady'], abbr['colspan'], abbr['rowspan']
            iframe.grid(column=col, row=row, sticky=sticky, padx=padx, pady=pady, columnspan=colspan, rowspan=rowspan) # yapf:disable

        self.iframe[0].columnconfigure(0, weight=1)
        self.iframe[0].columnconfigure(1, weight=8)
        self.iframe[0].rowconfigure([0,1], weight=0)
        self.iframe[1].columnconfigure(0,weight=1)
        self.iframe[1].rowconfigure(0, weight=0)
        self.iframe[1].rowconfigure(1, weight=1)
        self.iframe[2].columnconfigure(0, weight=1)
        self.iframe[2].rowconfigure([0,1], weight=1)
        self.iframe[2].rowconfigure([2,3,4], weight=1)

        #【TabFrame_1.labelframe1.labelframe1, TabFrame_1.labelframe1.labelframe2, TabFrame_1.labelframe1.labelframe3】
        #【TabFrame_1.labelframe2.labelframe1, TabFrame_1.labelframe2.labelframe2】
        #【TabFrame_1.labelframe3.labelframe1, TabFrame_1.labelframe3.labelframe2, TabFrame_1.labelframe3.labelframe3, TabFrame_1.labelframe3.labelframe4, TabFrame_1.labelframe3.labelframe5】
        self.iframe_sub = [[], [], []]
        for idx, mainframe in enumerate(self.iframe_sub):
            for _, parm in enumerate(parms[idx]['subframe']):
                text = parm['text']
                mainframe.append(tk.LabelFrame(master=self.iframe[idx], text=text)) # yapf:disable
            for idx_sub, subframe in enumerate(mainframe):
                abbr = parms[idx]['subframe'][idx_sub]
                col, row, sticky  = abbr['col'], abbr['row'], abbr['sticky']
                padx, pady, colspan, rowspan = abbr['padx'], abbr['pady'], abbr['colspan'], abbr['rowspan']
                subframe.grid(column=col, row=row, sticky=sticky, padx=padx, pady=pady, columnspan=colspan, rowspan=rowspan) # yapf:disable

        #【TabFrame_1.labelframe1.labelframe1, TabFrame_1.labelframe1.labelframe2, TabFrame_1.labelframe1.labelframe3】
        self.one_radiobtn_val = tk.IntVar()
        self.one_radiobtn = []
        for idx, parm in enumerate(parms[0]['radiobutton']):
            text = parm['text']
            font = ('microsoft yahei', 10, 'bold underline')
            command = (lambda e=None:self.one_radiobtn_select_changed(e))
            self.one_radiobtn.append(tk.Radiobutton(master=self.iframe_sub[0][0], text=text, value=idx, variable=self.one_radiobtn_val, font=font, command=command )) # yapf:disable
        for idx, btn in enumerate(self.one_radiobtn):
            abbr = parms[0]['radiobutton'][idx]
            col, row, sticky, padx, pady = abbr['col'], abbr['row'], abbr['sticky'], abbr['padx'], abbr['pady']
            btn.grid(column=col, row=row, sticky=sticky, padx=padx, pady=pady)
        # self.one_radiobtn_val.set(0)
        # self.one_radiobtn[2].config(state='disable')
        # self.one_radiobtn[3].config(state='disable')

        abbr = parms[0]['combobox']
        abbr = abbr
        self.one_cbbox = ttk.Combobox(master=self.iframe_sub[0][1], values=abbr['values'], state=abbr['state']) # yapf:disable
        self.one_cbbox.grid(column=abbr['col'], row=abbr['row'], sticky=abbr['sticky'], padx=abbr['padx'], pady=abbr['pady']) # yapf:disable
        self.one_cbbox.current(0)

        abbr = parms[0]['button']
        abbr = abbr
        self.one_img = Image.open(os.path.join(os.curdir, 'icon', 'file.png')).resize((20,20),Image.ANTIALIAS)
        self.one_imgtk = ImageTk.PhotoImage(self.one_img)
        self.one_btn = tk.Button(master=self.iframe_sub[0][1], image=self.one_imgtk, width=abbr['width'], height=abbr['height'], borderwidth=abbr['borderwidth']) # yapf:disable
        self.one_btn.grid(column=abbr['col'], row=abbr['row'], sticky=abbr['sticky'], padx=abbr['padx'], pady=abbr['pady']) # yapf:disable
        self.one_cbbox.bind('<<ComboboxSelected>>', (lambda e=None: self.one_cbbox_select_changed(e)))
        self.one_btn.config(command=(lambda: self.one_btn_open()))

        entry_parm = parms[0]['entry']
        label_parm = parms[0]['label']
        # one_img = Image.open(os.path.join(os.curdir, 'icon', 'file.png')).resize((20,20),Image.ANTIALIAS)
        # one_imgtk = ImageTk.PhotoImage(one_img)
        self.one_entry_val = tk.StringVar()
        self.one_entry = ttk.Entry(master=self.iframe_sub[0][2], textvariable=self.one_entry_val, width=entry_parm['width']) # yapf:disable
        self.one_label = ttk.Label(master=self.iframe_sub[0][2], image=self.one_imgtk) # yapf:disable
        self.one_entry.grid(column=entry_parm['col'], row=entry_parm['row'], sticky=entry_parm['sticky'], padx=entry_parm['padx'], pady=entry_parm['pady']) # yapf:disable
        self.one_label.grid(column=label_parm['col'], row=label_parm['row'], sticky=label_parm['sticky'], padx=label_parm['padx'], pady=label_parm['pady']) # yapf:disable

        #【TabFrame_1.labelframe2.labelframe1, TabFrame_1.labelframe2.labelframe2】
        lbl1_parm = parms[1]['label_1']
        abbr = parms[1]['combobox']
        lbl2_parm = parms[1]['label_2']
        lbl3_parm = parms[1]['label_3']
        lbl4_parm = parms[1]['label_4']
        lbl5_parm = parms[1]['label_5']
        self.two_label_1 = tk.Label(master=self.iframe_sub[1][0], text=lbl1_parm['text'], justify =lbl1_parm['justify']) # yapf:disable
        self.two_cbbox = ttk.Combobox(master=self.iframe_sub[1][0], values=abbr['values'], state=abbr['state']) # yapf:disable
        self.two_label_2 = tk.Label(master=self.iframe_sub[1][0], text=lbl2_parm['text'], anchor=lbl2_parm['anchor']) # yapf:disable
        self.two_label_3 = tk.Label(master=self.iframe_sub[1][0], text=lbl3_parm['text'], relief=lbl3_parm['relief'], background=lbl3_parm['bg'], anchor=lbl3_parm['anchor']) # yapf:disable
        self.two_label_4 = tk.Label(master=self.iframe_sub[1][0], text=lbl4_parm['text'], anchor=lbl4_parm['anchor']) # yapf:disable
        self.two_label_5 = tk.Label(master=self.iframe_sub[1][0], text=lbl5_parm['text'], relief=lbl5_parm['relief'], background=lbl5_parm['bg'], anchor=lbl5_parm['anchor']) # yapf:disable
        self.two_label_1.grid(column=lbl1_parm['col'], row=lbl1_parm['row'], sticky=lbl1_parm['sticky'], padx=lbl1_parm['padx'], pady=lbl1_parm['pady']) # yapf:disable
        self.two_cbbox.grid(column=abbr['col'], row=abbr['row'], sticky=abbr['sticky'], padx=abbr['padx'], pady=abbr['pady']) # yapf:disable
        self.two_label_2.grid(column=lbl2_parm['col'], row=lbl2_parm['row'], sticky=lbl2_parm['sticky'], padx=lbl2_parm['padx'], pady=lbl2_parm['pady']) # yapf:disable
        self.two_label_3.grid(column=lbl3_parm['col'], row=lbl3_parm['row'], sticky=lbl3_parm['sticky'], padx=lbl3_parm['padx'], pady=lbl3_parm['pady']) # yapf:disable
        self.two_label_4.grid(column=lbl4_parm['col'], row=lbl4_parm['row'], sticky=lbl4_parm['sticky'], padx=lbl4_parm['padx'], pady=lbl4_parm['pady']) # yapf:disable
        self.two_label_5.grid(column=lbl5_parm['col'], row=lbl5_parm['row'], sticky=lbl5_parm['sticky'], padx=lbl5_parm['padx'], pady=lbl5_parm['pady']) # yapf:disable
        self.two_cbbox.current(1)

        btn1_parm = parms[1]['button_1']
        canvas_parm = parms[1]['canvas']
        btn2_parm = parms[1]['button_2']
        self.two_virtual_btn = tk.PhotoImage(width=1, height=1)
        self.two_virtual_img = tk.PhotoImage(width=1, height=1)
        self.two_btn_1 = tk.Button(master=self.iframe_sub[1][1], text='◀', image=self.two_virtual_btn, width=btn1_parm['width'], height=btn1_parm['height'], compound=btn1_parm['compound'], borderwidth=btn1_parm['borderwidth'], background=btn1_parm['background']) # yapf:disable
        self.two_canvas = tk.Canvas(master=self.iframe_sub[1][1]) # yapf:disable
        self.two_canvas.image = self.two_virtual_img
        self.two_canvas.create_image(0,0, anchor='center', image=self.two_virtual_img, tags="bg_img") # yapf:disable
        self.two_btn_2 = tk.Button(master=self.iframe_sub[1][1], text='▶', image=self.two_virtual_btn, width=btn2_parm['width'], height=btn2_parm['height'], compound=btn2_parm['compound'], borderwidth=btn2_parm['borderwidth'], background=btn2_parm['background']) # yapf:disable
        # self.two_btn_1.pack(side='left', expand=False)  # , anchor='w'
        # self.two_canvas.pack(side='left', expand=True, fill='both')
        # self.two_btn_2.pack(side='left', expand=False)
        self.two_btn_1.config(command=(lambda e=None: self.two_btn_left(e)))
        self.two_btn_2.config(command=(lambda e=None: self.two_btn_right(e)))
        self.two_btn_1.grid(column=btn1_parm['col'], row=btn1_parm['row'], sticky=btn1_parm['sticky']) # yapf:disable
        self.two_canvas.grid(column=canvas_parm['col'], row=canvas_parm['row'], sticky=canvas_parm['sticky']) # yapf:disable
        self.two_btn_2.grid(column=btn2_parm['col'], row=btn2_parm['row'], sticky=btn2_parm['sticky']) # yapf:disable

        self.hide_widget(self.iframe_sub[0][2])
        self.hide_widget(self.two_btn_1)
        self.hide_widget(self.two_btn_2)
        self.two_canvas.bind('<Configure>', (lambda e=None:self.show_canvas(e)))


        self.iframe_sub[1][0].columnconfigure([0], weight=0)
        self.iframe_sub[1][0].columnconfigure([1], weight=1)
        self.iframe_sub[1][0].rowconfigure([0,1,2], weight=1)
        self.iframe_sub[1][1].columnconfigure([0,2], weight=0)
        self.iframe_sub[1][1].columnconfigure([1], weight=1)
        self.iframe_sub[1][1].rowconfigure([0], weight=1)

    def one_radiobtn_select_changed(self, event):
        self.clear_file_info()
        parms = self.parms
        if self.one_radiobtn_val.get() == 0 or self.one_radiobtn_val.get() == 1:
            self.hide_widget(self.iframe_sub[0][2])
            idx = 1
            abbr = parms[0]['subframe'][idx]
            col, row, sticky = abbr['col'], abbr['row'], abbr['sticky']
            padx, pady, colspan, rowspan = abbr['padx'], abbr['pady'], abbr['colspan'], abbr['rowspan']
            self.iframe_sub[0][idx].grid(column=col, row=row, sticky=sticky, padx=padx, pady=pady, columnspan=colspan, rowspan=rowspan)
        elif self.one_radiobtn_val.get() == 2:
            self.hide_widget(self.iframe_sub[0][1])
            self.hide_widget(self.iframe_sub[0][2])
        elif self.one_radiobtn_val.get() == 3:
            self.hide_widget(self.iframe_sub[0][1])
            idx = 2
            abbr = parms[0]['subframe'][idx]
            col, row, sticky = abbr['col'], abbr['row'], abbr['sticky']
            padx, pady, colspan, rowspan = abbr['padx'], abbr['pady'], abbr['colspan'], abbr['rowspan']
            self.iframe_sub[0][idx].grid(column=col, row=row, sticky=sticky, padx=padx, pady=pady, columnspan=colspan, rowspan=rowspan)

    def one_cbbox_select_changed(self, event):
        if self.one_cbbox.current() == 0:
            img = Image.open(os.path.join(os.curdir, 'icon', 'file.png')).resize((20,20),Image.ANTIALIAS)
            imgtk = ImageTk.PhotoImage(img)
            self.one_btn.image = imgtk
            self.one_btn.config(image=imgtk)
        elif self.one_cbbox.current() == 1:
            img = Image.open(os.path.join(os.curdir, 'icon', 'folder-home-open.png')).resize((20,20),Image.ANTIALIAS)
            imgtk = ImageTk.PhotoImage(img)
            self.one_btn.image = imgtk
            self.one_btn.config(image=imgtk)

    def one_btn_open(self):
        self.clear_file_info()

        title = ['select image files', 'select video files', 'select image directory', 'select video directory']
        filetypes = [[("image file", "*.jpg"),("image file", "*.png"),("image file", "*.gif")],
                     [("video file", "*.mov"),("video file", "*.ts"),("video file", "*.avi"),("video file", "*.mpeg"),("video file", "*.mp4")]]
        initialdir = os.curdir
        file_extend = [('*.jpg', '*.png', '*.gif'), ('*.mov','*.ts','*.avi','*.mpeg','*.mp4')]

        if self.one_cbbox.current() == 0:
            if self.one_radiobtn_val.get() == 0:
                self.files = fd.askopenfilenames(title=title[0], filetypes=filetypes[0], initialdir=initialdir)
            elif self.one_radiobtn_val.get() == 1:
                self.files = fd.askopenfilenames(title=title[1], filetypes=filetypes[1], initialdir=initialdir)
        elif self.one_cbbox.current() == 1:
            if self.one_radiobtn_val.get() == 0:
                self.folder_path = fd.askdirectory(title=title[2], initialdir=initialdir)
                [ self.files.extend(glob.glob( os.path.abspath(os.path.join(self.folder_path, ext)))) for ext in file_extend[0] ]
            elif self.one_radiobtn_val.get() == 1:
                self.folder_path = fd.askdirectory(title=title[3], initialdir=initialdir)
                [ self.files.extend(glob.glob( os.path.abspath(os.path.join(self.folder_path, ext)))) for ext in file_extend[1] ]
        if len(self.files) == 0:
            msgbox.showwarning('Warning', 'Failed to open file')
            return

        self.file_path = os.path.abspath(self.files[self.files_idx])
        self.folder_name = os.path.dirname(self.file_path)
        self.file_name = os.path.basename(self.file_path)
        self.show_file_info()

    def show_file_info(self):
        self.two_label_3.config(text=self.folder_name)
        self.two_label_5.config(text=self.file_name)

        if len(self.files) > 1:
            parms = self.parms
            btn1_parm = parms[1]['button_1']
            btn2_parm = parms[1]['button_2']
            self.two_btn_1.grid(column=btn1_parm['col'], row=btn1_parm['row'], sticky=btn1_parm['sticky']) # yapf:disable
            self.two_btn_2.grid(column=btn2_parm['col'], row=btn2_parm['row'], sticky=btn2_parm['sticky']) # yapf:disable
            if self.one_radiobtn_val.get() == 0:
                self.show_canvas(event=None)
        else:
            self.hide_widget(self.two_btn_1)
            self.hide_widget(self.two_btn_2)

            if self.one_radiobtn_val.get() == 0:
                self.show_canvas(event=None)
            elif self.one_radiobtn_val.get() == 1:
                pass
            elif self.one_radiobtn_val.get() == 2:
                pass
            elif self.one_radiobtn_val.get() == 3:
                pass

    def clear_file_info(self):
        self.files_idx = 0
        self.files = []
        self.folder_name = ''
        self.file_name = ''
        self.file_path = ''
        self.two_label_3.config(text='')
        self.two_label_5.config(text='')
        self.two_canvas.delete('all')
        self.two_canvas.update()
        self.hide_widget(self.two_btn_1)
        self.hide_widget(self.two_btn_2)

    def show_canvas(self, event):
        if len(self.files)>0 and self.one_radiobtn_val.get()==0:
            img_bgr = cv2.imread(self.file_path)
            imgtk = self.get_imgtk(img_bgr)
            self.two_canvas.image = imgtk
            w = self.two_canvas.winfo_width()
            h = self.two_canvas.winfo_height()
            self.two_canvas.create_image(w/2,h/2, anchor='center', image=imgtk, tags="bg_img")
            self.two_canvas.update()

    def two_btn_left(self, event):
        if len(self.files)==0:
            return
        if self.files_idx == 0:
            self.files_idx = len(self.files)-1
        else:
            self.files_idx -= 1
        self.file_path = os.path.abspath(self.files[self.files_idx])
        self.folder_name = os.path.dirname(self.file_path)
        self.file_name = os.path.basename(self.file_path)
        self.show_file_info()

    def two_btn_right(self, event):
        if len(self.files)==0:
            return
        if self.files_idx == (len(self.files)-1):
            self.files_idx = 0
        else:
            self.files_idx += 1
        self.file_path = os.path.abspath(self.files[self.files_idx])
        self.folder_name = os.path.dirname(self.file_path)
        self.file_name = os.path.basename(self.file_path)
        self.show_file_info()

    def get_imgtk(self, img_bgr):
        img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        im = Image.fromarray(img)
        height, width = img.shape[:2]
        if width > (self.win.winfo_width()/2) or height > (self.win.winfo_height()*2/3):
            width_ratio = (self.win.winfo_width()/2) / width
            height_ratio = (self.win.winfo_height()*2/3) / height
            ratio = min(width_ratio, height_ratio)

            width, height = int(width*ratio), int(height*ratio)
            width = ( 1 if width<=0 else width )
            height = ( 1 if height<=0 else height )
            im = im.resize((width, height), Image.ANTIALIAS)
        imgtk = ImageTk.PhotoImage(image=im)
        return imgtk

    def hide_widget(self, widget):
        widget.grid_forget()
        widget.update()

    def show_widget(self, widget):
        widget.grid()
        widget.update()

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
    t1 = TabFrame_1(win, tab1)
    win.protocol("WM_DELETE_WINDOW", lambda e=None, w=win:destroy_window(e, w))
    win.mainloop()


if __name__ == '__main__':
    # main()
    pass
