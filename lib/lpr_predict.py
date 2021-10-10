import os
import tkinter as tk

import cv2
import imutils
import numpy as np
import pytesseract
from PIL import Image, ImageTk


class ImageProcessing:
    def __init__(self, win:tk.Tk):
        self.win = win
        self.__win_witdh = self.win.winfo_width()
        self.__win_height = self.win.winfo_height()

    def cv2pil(img_bgr):
        new_img = img_bgr.copy()
        if new_img.ndim == 2:
            pass
        elif new_img.shape[2] == 3:
            new_img = cv2.cvtColor(new_img, cv2.COLOR_BGR2RGB)
        elif new_img.shape[2] == 4:
            new_img = cv2.cvtColor(new_img, cv2.COLOR_BGRA2RGBA)
        pil_img = Image.fromarray(new_image)
        return pil_img

    def pil2cv(img_rgb):
        cv_img = np.array(img_rgb, dtype=np.uint8)
        if new_img.ndim == 2:
            pass
        elif new_img.shape[2] == 3:
            cv_img = cv2.cvtColor(cv_img, cv2.COLOR_RGB2BGR)
        elif new_img.shape[2] == 4:
            cv_img = cv2.cvtColor(cv_img, cv2.COLOR_RGBA2BGRA)
        return cv_img

    def get_imgbgr(self, filename):
        '''
        cv2.IMREAD_COLOR: 此為預設值，這種格式會讀取 RGB 三個 channels 的彩色圖片，而忽略透明度的 channel。
        cv2.IMREAD_GRAYSCALE: 以灰階的格式來讀取圖片。
        cv2.IMREAD_UNCHANGED: 讀取圖片中所有的 channels，包含透明度的 channel。
        '''
        img_bgr = None
        img_bgr = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
        img_bgr = cv2.imdecode(np.fromfile(filename, dtype=np.uint8), cv2.IMREAD_UNCHANGED) if img_bgr is None else img_bgr
        return img_bgr

    def get_imgresize_by_imutils(self, img_bgr, width=512):
        return imutils.resize(img_bgr, width)

    def get_imgresize_by_cv2(self, img_bgr, width, height):
        '''
        如果是要縮小圖片的話，通常 INTER_AREA 使用效果較佳。
        如果是要放大圖片的話，通常 INTER_CUBIC 使用效果較佳，次等則是 INTER_LINEAR。
        如果要追求速度的話，通常使用 INTER_NEAREST。
        '''
        img_re = img_bgr
        height, width = img.shape[:2]
        if width > self.__win_witdh or height > self.__win_height:
            w_ratio = self.__win_witdh / width
            h_ratio = self.__win_height / height
            ratio = min(w_ratio, h_ratio)
            width, height = int(width*ratio), int(height*ratio)
            width = (1 if width <= 0 else width)
            height = (1 if height <= 0 else height)
            img_re = cv2.resize(img_re, (width, height), interpolation=interpolation) # yapf:disable
        return img_re

    def get_imgtk(self, img_bgr):
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        im = Image.fromarray(img_rgb)
        imgtk = ImageTk.PhotoImage(image=im)
        return imgtk

    def get_imgtk_by_ratio(self, img_bgr, w_ratio=1/2, h_ratio=2/3):
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        im = Image.fromarray(img_rgb)
        height, width = im.shape[:2]
        if width > self.__win_witdh or height > self.__win_height:
            width_ratio = (self.__win.winfo_width() * w_ratio) / width
            height_ratio = (self.__win.winfo_height() * h_ratio) / height
            ratio = min(width_ratio, height_ratio)
            width, height = int(width * ratio), int(height * ratio)
            width = (1 if width <= 0 else width)
            height = (1 if height <= 0 else height)
            im = im.resize((width, height), Image.ANTIALIAS)
        return im

    def get_imgsharpen(self, img_bgr):
        # sigma = 5, 15, 25
        blur_img = cv2.GaussianBlur(img_bgr, (0, 0), sigmaX=5)
        usm_img = cv2.addWeighted(src1=img_bgr, alpha=1.5, src2=blur_img, beta=-0.5, gamma=0) # yapf:disable
        blur_img = cv2.GaussianBlur(usm_img, (0, 0), sigmaX=15)
        usm_img = cv2.addWeighted(src1=usm_img, alpha=1.5, src2=blur_img, beta=-0.5, gamma=0) # yapf:disable
        blur_img = cv2.GaussianBlur(usm_img, (0, 0), sigmaX=25)
        usm_img = cv2.addWeighted(src1=usm_img, alpha=1.5, src2=blur_img, beta=-0.5, gamma=0) # yapf:disable
        blur_img = cv2.GaussianBlur(usm_img, (0, 0), sigmaX=25)
        usm_img = cv2.addWeighted(src1=usm_img, alpha=1.5, src2=blur_img, beta=-0.5, gamma=0) # yapf:disable
        h, w = img_bgr.shape[:2]
        sharpen_img = np.zeros([h, w, 3], dtype=img_bgr.dtype)
        sharpen_img[0:h,0:w,:] = usm_img
        return sharpen_img

    def plate_detection(self, mthd:1):
        pass

    def plate_alignment(self, imgbgr):
        pass

    def ocr(self, img_bgr, lang='eng'):
        '''
        lang: eng, chi_tra, chi_sim
        '''
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        # img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'
        result = pytesseract.image_to_string(img_rgb, lang=lang) # yapf:disable
        return result

    def svm(self, img_bgr):
        result = ''
        return result

    def cnn(self, img_bgr):
        result = ''
        return result

    def plate_recognition(self, img_bgr, mthd:2):
        result = ''
        if mthd == 1:
            img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
            result = ocr(img_rgb, lang='chi_sim')
        elif mthd == 2:
            result = svm(img_bgr)
        elif mthd == 3:
            result == cnn(img_bgr)
        return result


def main():
    win = tk.Tk()
    win.geometry("1024x768")
    win.update()
    ips = ImageProcessing(win=win)
    win.destroy()

    src_file = os.path.join(os.path.abspath(os.path.curdir), 'source', '3.jpg')
    if not os.path.exists(src_file):
        return
    print(src_file)
    img_bgr = ips.get_imgbgr(src_file)
    usm = ips.get_imgsharpen(img_bgr)
    img_gray = cv2.cvtColor(usm, cv2.COLOR_BGR2GRAY)
    h,w = img_bgr.shape[:2]
    result = np.zeros([h, w*2, 3], dtype=img_bgr.dtype)
    result[0:h, 0:w, :] = img_bgr
    result[0:h, w:2 * w, :] = usm
    cv2.imshow("gray_image", img_gray)
    cv2.waitKey(0)
    cv2.imshow("sharpen_image", result)
    cv2.waitKey(0)


    cv2.destroyAllWindows()
    text = ips.ocr(usm)
    print(text)


    # pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'
    # result = pytesseract.image_to_string(img_rgb, lang='eng')  #eng, chi_tra,chi_sim
    # print(result)


if __name__ == '__main__':
    main()
    pass
