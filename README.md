# LPR-GUI-TKINTER

從車牌辨識學習視窗程式 - Tkinter

- 串接 車牌辨識系統
- 連結 資料庫 或 CSV
- 連結 設定檔
- 連結 Shell 視窗

# Getting Started

## 系統需求

- `Python 3.0+`, `Git 2.0+`
  > 若要使用 `Visual Studio code` 執行，需要裝 `Python`, `Code Runner`。
  >
  > > [補充] `Visual Studio code` 安裝
  > >
  > > 1.  `Markdown Preview Github Styling`
  > > 2.  `Auto-Open Markdown Preview`

> > 上述兩者擇一，即可在編輯 `ReadMe.md` 並即時顯示

## 安裝套件

- 依使用者 `Python 版本`， 安裝下列`Python 版本`對應的`指令`

```
py -3.9 -m pip install -U --force-reinstall numpy imutils Cython opencv-python tensorflow keras
py -3.8 -m pip install -U --force-reinstall numpy imutils Cython opencv-python tensorflow keras
py -3.6 -m pip install -U --force-reinstall numpy imutils Cython opencv-python tensorflow==1.15 tensorflow-gpu==1.15 keras
py -3.6 -m pip install -U h5py==2.10.0 --force-reinstall

py -3.6 -m pip install --upgrade pip
py -3.6 -m pip install -U --force-reinstall opencv-python opencv-contrib-python
py -3.6 -m pip install -U --force-reinstall msvc-runtime easyocr
py -3.6 -m pip install -U torch==1.4.0+cpu torchvision==0.5.0+cpu

py -3.6 -m pip install -U pytesseract
```

## 程式執行

1. 切入程式放置資料夾
2. 同時點選 `滑鼠右鍵` 和 `鍵盤Shift`
3. 點擊 `在這裡開啟 Powershell 視窗` 或 `在這裡開啟 CMD 視窗`
4. 在 `Powershell` 或 `CMD` 輸入下列程式命令

```
python demo.py
```

或

```
py -3.6 demo.py
```

## 參考網站
1. 影像處理基礎
- [Python 與 OpenCV 基本讀取、顯示與儲存圖片教學](https://blog.gtwang.org/programming/opencv-basic-image-read-and-write-tutorial/)
- [Python 影像辨識筆記目錄](https://yanwei-liu.medium.com/computer-vision-with-python-569dc58aff22)
- [【OpenCV-Python 系列 Ⅳ】基礎影像處理集合包](https://grady1006.medium.com/opencv-python%E7%B3%BB%E5%88%97%E2%85%B3-%E5%9F%BA%E7%A4%8E%E5%BD%B1%E5%83%8F%E8%99%95%E7%90%86%E9%9B%86%E5%90%88%E5%8C%85-6c46fb2744ab)
- [影像處理--影像特效](https://iter01.com/519620.html)
2. 數字辨識
- [影像辨識-古佳怡](https://ct.fg.tp.edu.tw/wp-content/uploads/2017/06/%E5%BD%B1%E5%83%8F%E8%BE%A8%E8%AD%98.pdf)
- [Tesseract-ocr installer](https://github.com/UB-Mannheim/tesseract/wiki)
- [Tesseract-ocr tessdata](https://github.com/tesseract-ocr/tessdata)
- [EasyOCR](https://www.gushiciku.cn/pl/g85G/zh-tw)
3. 影像處理進階
- [[影象處理] Python+OpenCV 實現車牌區域識別及 Sobel 運算元](https://iter01.com/90662.html)
- [python 中值濾波去除反光\_Python 實現中值濾波、均值濾波的方法](https://blog.csdn.net/weixin_35698059/article/details/113650706)
- [python 中值濾波去除反光\_數學之路-python 計算實戰(17)-機器視覺-濾波去噪(中值濾波)](https://blog.csdn.net/weixin_32379547/article/details/113650705)
4. 影像光亮處理
- [Opencv 去高光或鏡面反射（illuminationChange）\_jacke121 的專欄-程序員宅基地](http://www.cxyzjd.com/article/jacke121/95736092)
- [error: (-215:Assertion failed) npoints >= 0 && (depth == CV_32F || depth == CV_32S) in function '...](https://www.jianshu.com/p/f7930023dc62)
- [【沒錢 ps,我用 OpenCV!】Day 1 - 總是要從安裝 OpenCV 開始 + 電腦中圖片的基本概念(灰階、全彩 RGB、座標軸、計算圖片大小)](https://ithelp.ithome.com.tw/articles/10235551)
- [【沒錢 ps,我用 OpenCV!】Day 9 - 日系濾鏡 6，運用 OpenCV 降低圖片的高光 reduce highlights](https://ithelp.ithome.com.tw/articles/10240334)
- [[Day19]Matplotlib 讓資料視覺化！](https://ithelp.ithome.com.tw/articles/10196239)
- [无缝融合 seamlessClone()，调试颜色 colorChange()，消除高亮 illuminationChange()，纹理扁平化 textureFlattening()（OpenCV 案例源码 cloning_demo.cpp 解读](https://www.cnblogs.com/xixixing/p/12335317.html)
5. 車牌影像處理AI
- [Tensorflow+CNN實現車牌識別](https://www.twblogs.net/a/5c80a415bd9eee35cd693981)
- [透視變換Perspective Transformation](https://blog.csdn.net/xiaowei_cqu/article/details/26471527)
- [透視變換Perspective Transformation 續](https://blog.csdn.net/xiaowei_cqu/article/details/26478135)
## 參考網站[理論]

- [影像辨識處理](https://www.smasoft-tech.com/show/knowledgebase-shemeshiyingxiangqianchuli.htm)
- [Image Algorithm](http://web.ntnu.edu.tw/~algo/Image.html)
- [DNN車牌辨識技術與應用](http://www.twcloud.org.tw/files/file_pool/1/0J365497692777195097/2019%20TASA%2012%E6%9C%88%E7%B0%A1%E5%A0%B1_DNN%E8%BB%8A%E7%89%8C%E8%BE%A8%E8%AD%98%E6%8A%80%E8%A1%93%E8%88%87%E6%87%89%E7%94%A8.pdf)
- [傳統車牌辨識 vs AI車牌辨識](http://blog.udn.com/yccsonar/154776636)