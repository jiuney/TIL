from tkinter import *
from tkinter.simpledialog import *
from tkinter.filedialog import *
import math
import os
import os.path
import struct
import csv
import xlrd
import xlwt
import xlsxwriter
import time
from PIL import Image, ImageFilter, ImageEnhance, ImageOps
from PIL.ImageFilter import GaussianBlur
import PIL.ImageOps





#####################
##### 함수 선언부 #####
#####################

def openImagePIL():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH,outW

    filename = askopenfilename(parent=window,
                               filetypes=(("컬러 파일", "*.jpg;*.png;*.bmp;*.tif"), ("모든 파일", "*.*")))
    if filename == "" or filename == None:
        return

    inImage = Image.open(filename)
    inW = inImage.width
    inH = inImage.height

    outImage = inImage.copy()
    outW = outImage.width
    outH = outImage.height

    displayImagePIL()

def displayImagePIL():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW

    if canvas!= None:    # 예전에 실행한 적이 있다면
        canvas.destroy()

    VIEW_X = outW
    VIEW_Y = outH
    step = 1

    window.geometry(str(int(VIEW_Y*1.2)) + "x" + str(int(VIEW_X*1.2)))
    canvas = Canvas(window, height=VIEW_Y, width=VIEW_Y)
    paper = PhotoImage(height=VIEW_Y, width=VIEW_Y)
    canvas.create_image((VIEW_X // 2, VIEW_Y // 2), image=paper, state="normal")
    import numpy
    rgbImage = outImage.convert("RGB")
    # 성능 개선
    rgbStr = ""    # 전체 픽셀의 문자열을 저장
    for i in numpy.arange(0, outH, step):
        tmpStr = ""
        for k in numpy.arange(0, outW, step):
            i = int(i)
            k = int(k)
            r, g, b = rgbImage.getpixel((k, i))
            tmpStr += " #%02x%02x%02x" % (r, g, b)    # 문자열에서 한 칸을 꼭 떼 줘야 나중에 자를 수 있다
        rgbStr += "{" + tmpStr + "} "     # 문자열에서 중괄호 끝에 한 칸을 꼭 떼 줘야 나중에 자를 수 있다
    paper.put(rgbStr)    # 문자열을 put하면 차례로 들어간다
    canvas.pack(expand=1, anchor=CENTER)
    # 이미지 정보
    status.configure(text = "이미지 정보: " + str(outW) + "x" + str(outH))

def saveImagePIL():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW

    if outImage == None:
        return

    saveFp = asksaveasfile(parent=window, mode='wb', defaultextension="*.jpg",
                           filetypes=(("JPG 파일", "*.jpg"), ("모든 파일", "*.*")))
    if saveFp == "" or saveFp == None:
        return

    outImage.save(saveFp.name)
    print("Save.")





################################################
##### 컴퓨터 비전 (영상 처리) 알고리즘 함수 모음 #####
################################################

def addminusImagePIL():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW

    value = askfloat("밝게/어둡게 하기", "값 (0 ~ 16)", minvalue=0.0, maxvalue=16.0)   # 1이 본전, 0~1이 어둡게, 1 초과가 밝게

    outImage = inImage.copy()
    outImage = ImageEnhance.Brightness(outImage).enhance(value)

    outW = outImage.width
    outH = outImage.height

    displayImagePIL()

def invertImagePIL():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW

    outImage = inImage.copy()
    outImage = PIL.ImageOps.invert(outImage)

    outW = outImage.width
    outH = outImage.height

    displayImagePIL()

def posterizeImagePIL():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW

    bVal = askinteger("포스터화", "값 (1 ~ 8)", minvalue=1, maxvalue=8)

    outImage = inImage.copy()
    outImage = ImageOps.posterize(outImage, bVal)

    outW = outImage.width
    outH = outImage.height

    displayImagePIL()


































def morphImagePIL():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW

    filename2 = askopenfilename(parent=window,
                               filetypes=(("컬러 파일", "*.jpg;*.png;*.bmp;*.tif"), ("모든 파일", "*.*")))
    if filename == "" or filename == None:
        return

    inImage2 = Image.open(filename2)

    aVal = askfloat("가중치", "값 (0.0 ~ 1.0)", minvalue=0.0, maxvalue=1.0)

    outImage = Image.blend(inImage, inImage2, alpha=aVal)

    outW = outImage.width
    outH = outImage.height

    displayImagePIL()

def blurImagePIL():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW

    outImage = inImage.copy()
    outImage = outImage.filter(ImageFilter.BLUR)

    outW = outImage.width
    outH = outImage.height

    displayImagePIL()

def sharpenImagePIL():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW

    outImage = inImage.copy()
    outImage = outImage.filter(ImageFilter.SHARPEN)

    outW = outImage.width
    outH = outImage.height

    displayImagePIL()

def contourImagePIL():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW

    outImage = inImage.copy()
    outImage = outImage.filter(ImageFilter.CONTOUR)

    outW = outImage.width
    outH = outImage.height

    displayImagePIL()

def edgeImagePIL():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW

    outImage = inImage.copy()
    outImage = outImage.filter(ImageFilter.FIND_EDGES)

    outW = outImage.width
    outH = outImage.height

    displayImagePIL()

def embossImagePIL():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW

    outImage = inImage.copy()
    outImage = outImage.filter(ImageFilter.EMBOSS)

    outW = outImage.width
    outH = outImage.height

    displayImagePIL()

def gaussImagePIL():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW

    r = askinteger("가우시안 블러", "값 (0 ~ 100)", minvalue=0, maxvalue=360)

    outImage = inImage.copy()
    outImage = outImage.filter(GaussianBlur(radius=r))

    outW = outImage.width
    outH = outImage.height

    displayImagePIL()

def zoominImagePIL():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW

    scale = askinteger("확대", "값 (2 ~ 8)", minvalue=2, maxvalue=8)

    outImage = inImage.copy()
    outImage = outImage.resize((inH*scale, inW*scale))

    outW = outImage.width
    outH = outImage.height

    displayImagePIL()

def zoomoutImagePIL():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW

    scale = askinteger("축소", "값 (2 ~ 8)", minvalue=2, maxvalue=8)

    outImage = inImage.copy()
    outImage = outImage.resize((inH//scale, inW//scale))

    outW = outImage.width
    outH = outImage.height

    displayImagePIL()


def rotateImagePIL():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW

    angle = askinteger("회전", "각도 (0 ~ 360)", minvalue=0, maxvalue=360)

    outImage = inImage.copy()
    outImage = outImage.rotate(angle)

    displayImagePIL()

# def resizeImagePIL():
#     global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
#
#     vw = askinteger("가로 크기", "픽셀(1~2000)", minvalue=1, maxvalue=2000)
#     vh = askinteger("세로 크기", "픽셀(1~2000)", minvalue=1, maxvalue=2000)
#
#     outImage = inImage.copy()
#     outImage = outImage.resize((vh, vw))
#
#     outW = outImage.width
#     outH = outImage.height
#
#     displayImagePIL()                     #################################### 뭔가 이상함 ㅠㅠ

def updownImagePIL():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW

    outImage = inImage.copy()
    outImage = outImage.transpose(Image.FLIP_TOP_BOTTOM)

    outW = outImage.width
    outH = outImage.height

    displayImagePIL()

def leftrightImagePIL():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW

    outImage = inImage.copy()
    outImage = outImage.transpose(Image.FLIP_LEFT_RIGHT)

    outW = outImage.width
    outH = outImage.height

    displayImagePIL()



















##########################
##### 전역 변수 선언부 #####
##########################

inImage, outImage = None, None
inH, inW, outH, outW, dispW, dispH = [0] * 6

window, canvas, paper = None, None, None
filename = ""

VIEW_X, VIEW_Y = 512, 512 # 화면에 보일 크기 (출력용)





#####################
##### 메인 코드부 #####
#####################

window = Tk()
window.geometry("500x500")
window.title("컴퓨터 비전 (컬러 라이브러리) Ver 0.01")

status = Label(window, text = "이미지 정보: ", bd = 1, relief = SUNKEN, anchor = W)
status.pack(side=BOTTOM, fill=X)



mainMenu = Menu(window)
window.config(menu=mainMenu)

fileMenu = Menu(mainMenu)
mainMenu.add_cascade(label="파일", menu=fileMenu)
fileMenu.add_command(label="파일 열기", command=openImagePIL)
fileMenu.add_separator()
fileMenu.add_command(label="파일 저장", command=saveImagePIL)

comVisionMenu1 = Menu(mainMenu)
mainMenu.add_cascade(label="화소점 처리", menu=comVisionMenu1)
comVisionMenu1.add_command(label="밝게/어둡게 하기", command=addminusImagePIL)
comVisionMenu1.add_command(label="화소값 반전", command=invertImagePIL)
comVisionMenu1.add_command(label="Posterization", command=posterizeImagePIL)
comVisionMenu1.add_separator()
comVisionMenu1.add_command(label="모핑", command=morphImagePIL)

comVisionMenu2 = Menu(mainMenu)
mainMenu.add_cascade(label="화소 영역 처리", menu=comVisionMenu2)
comVisionMenu2.add_command(label="블러 처리", command=blurImagePIL)
comVisionMenu2.add_command(label="샤프닝 처리", command=sharpenImagePIL)
comVisionMenu2.add_command(label="윤곽 표시", command=contourImagePIL)
comVisionMenu2.add_command(label="경계선 검출", command=edgeImagePIL)
comVisionMenu2.add_command(label="엠보싱 처리", command=embossImagePIL)
comVisionMenu2.add_command(label="가우시안 필터링", command=gaussImagePIL)

comVisionMenu3 = Menu(mainMenu)
mainMenu.add_cascade(label="기하학 처리", menu=comVisionMenu3)
comVisionMenu3.add_command(label="확대", command=zoominImagePIL)
comVisionMenu3.add_command(label="축소", command=zoomoutImagePIL)
comVisionMenu3.add_command(label="회전", command=rotateImagePIL)
# comVisionMenu3.add_command(label="크기 조절", command=resizeImagePIL)
comVisionMenu3.add_command(label="상하 반전", command=updownImagePIL)
comVisionMenu3.add_command(label="좌우 반전", command=leftrightImagePIL)



window.mainloop()
