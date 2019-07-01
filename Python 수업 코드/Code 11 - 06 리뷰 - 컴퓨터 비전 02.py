
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


#####################
##### 함수 선언부 #####
#####################

def malloc(h, w, initValue=0):    # malloc = memory allocate
    retMemory = []
    for _ in range (h):
        tmpList = []
        for _ in range (w):
            tmpList.append(initValue)
        retMemory.append(tmpList)
    return retMemory

def loadImage(fname):
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    fsize = os.path.getsize(fname)    # 파일의 크기 (바이트)
    inH = inW = int(math.sqrt(fsize))    # 핵심 코드
    # 입력 영상 메모리 확보
    inImage = []
    inImage = malloc(inH, inW)
    # 파일에서 메모리로 가져오기
    with open(fname, "rb") as rFp:  # rb = binary
        for i in range (inH):
            for k in range (inW):
                inImage[i][k] = int(ord(rFp.read(1)))

def openImage():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH,outW
    filename = askopenfilename(parent=window,
                               filetypes=(("RAW 파일", "*.raw"), ("모든 파일", "*.*")))
    if filename == "" or filename == None:
        return
    loadImage(filename)
    equalImage()

def displayImage():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global VIEW_X, VIEW_Y
    if canvas!= None:    # 예전에 실행한 적이 있다면
        canvas.destroy()
    # 고정된 화면 크기
    if outH <= VIEW_Y or outW <= VIEW_X:
        VIEW_X = outW
        VIEW_Y = outH
        step = 1
    else:
        VIEW_X = 512
        VIEW_Y = 512
        step = outW / VIEW_X
    window.geometry(str(int(VIEW_Y*1.2)) + "x" + str(int(VIEW_X*1.2)))
    canvas = Canvas(window, height=VIEW_Y, width=VIEW_Y)
    paper = PhotoImage(height=VIEW_Y, width=VIEW_Y)
    canvas.create_image((VIEW_X // 2, VIEW_Y // 2), image=paper, state="normal")
    import numpy
    # 성능 개선
    rgbStr = ""    # 전체 픽셀의 문자열을 저장
    for i in numpy.arange(0, outH, step):
        tmpStr = ""
        for k in numpy.arange(0, outW, step):
            i = int(i)
            k = int(k)
            r = g = b = outImage[i][k]
            tmpStr += " #%02x%02x%02x" % (r, g, b)    # 문자열에서 한 칸을 꼭 떼 줘야 나중에 자를 수 있다
        rgbStr += "{" + tmpStr + "} "     # 문자열에서 중괄호 끝에 한 칸을 꼭 떼 줘야 나중에 자를 수 있다
    paper.put(rgbStr)    # 문자열을 put하면 차례로 들어간다
    canvas.pack(expand=1, anchor=CENTER)
    # 이미지 정보
    status.configure(text = "이미지 정보: " + str(outW) + "x" + str(outH))

def equalImage():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정
    # 지금은 동일 영상이니까 크기 같음
    outH = inH
    outW = inW
    # 크기 결정되었으니 메모리 할당
    outImage = []
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘이 여기부터 시작
    for i in range(inH):
        for k in range(inW):
            outImage[i][k] = inImage[i][k]
    displayImage()

def addminusImage():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정
    # 지금은 동일 영상이니까 크기 같음
    outH = inH
    outW = inW
    # 크기 결정되었으니 메모리 할당
    outImage = []
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘이 여기부터 시작
    value = askinteger("밝게/어둡게 하기", "값 (-255 ~ 255)", minvalue=-255, maxvalue=255)
    for i in range(inH):
        for k in range(inW):
            v = inImage[i][k] + value
            if v > 255:
                v = 255
            elif v < 0:
                v = 0
            outImage[i][k] = v
    displayImage()




##########################
##### 전역 변수 선언부 #####
##########################

inImage, outImage = [], []
inH, inW, outH, outW, dispW, dispH = [0] * 6

window, canvas, paper = None, None, None
filename = ""

VIEW_X, VIEW_Y = 512, 512 # 화면에 보일 크기 (출력용)



#####################
##### 메인 코드부 #####
#####################

window = Tk()
window.geometry("500x500")
window.title("리뷰용 컴퓨터 비전 Ver 0.01")

status = Label(window, text = "이미지 정보: ", bd = 1, relief = SUNKEN, anchor = W)
status.pack(side=BOTTOM, fill=X)

mainMenu = Menu(window)
window.config(menu=mainMenu)

fileMenu = Menu(mainMenu)
mainMenu.add_cascade(label="파일", menu=fileMenu)
fileMenu.add_command(label="파일 열기", command=openImage)
fileMenu.add_separator()

comVisionMenu1 = Menu(mainMenu)
mainMenu.add_cascade(label="컴퓨터 비전", menu=comVisionMenu1)
comVisionMenu1.add_command(label="밝게/어둡게 하기", command=addminusImage)

window.mainloop()