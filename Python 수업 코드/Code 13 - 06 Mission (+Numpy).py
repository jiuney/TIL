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
import colorsys
import numpy as np
import pymysql





#####################
##### 함수 선언부 #####
#####################

def malloc(h, w, initValue = 0, dataType=np.uint8):
    tmpList = np.zeros((h, w), dtype = dataType).reshape(h, w)
    retMemory = np.array([tmpList, tmpList, tmpList])
    retMemory += initValue
    return retMemory

def loadImageColor(fname):
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW, photo

    inImage = []
    photo = Image.open(fname)    # PIL 객체
    inH = photo.height
    inW = photo.width

    # 메모리 확보
    inImage = malloc(inH, inW)

    photoRGB = photo.convert("RGB")

    # 참고: https://rfriend.tistory.com/289
    photoRGB = np.array(photoRGB).reshape(inH*inW, 3).T    # 구조를 바꿔서 2차원 배열로 바꾼 후에 행열을 뒤집어서 행이 열이 되고 열이 행이 되게 함. 이를 통해 r, g, b에 해당하는 번호들이 각각의 행에 들어가도록 함
    photoRGB = photoRGB.reshape(3, inH, inW)    # r, g, b 정보끼리 모았으니 이제 다시 3차원 배열로 바꿔줌.
    inImage = photoRGB

def openImageColor():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH,outW

    filename = askopenfilename(parent=window,
                               filetypes=(("컬러 파일", "*.jpg;*.png;*.bmp;*.tif"), ("모든 파일", "*.*")))
    if filename == "" or filename == None:
        return

    loadImageColor(filename)
    equalImageColor()
    displayImageColor()

def displayImageColor():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global VIEW_X, VIEW_Y

    if canvas!= None:    # 예전에 실행한 적이 있다면
        canvas.destroy()

    global VIEW_X, VIEW_Y
    # VIEW_X, VIEW_Y = 512, 512
    ## 고정된 화면 크기
    # 가로/세로 비율 계산

    if inW <= 512 and inH <= 512:  # 정방형 관계없이 둘다 512보다 작으면 그냥 사용
        VIEW_X = inH
        VIEW_Y = inW
    else:  # 한쪽이라도 512보다 크면
        ratio = inH / inW
        if ratio < 1:
            VIEW_X = int(512 * ratio)
            if inW > 512:
                VIEW_Y = 512
            else:
                VIEW_Y = inW
        elif ratio > 1:
            ratio = 1 / ratio
            if inH > 512:
                VIEW_X = 512
            else:
                VIEW_X = inH
            VIEW_Y = int(512 * ratio)
        else:
            if inH > 512:
                VIEW_X = 512
            else:
                VIEW_X = inH
            if inW > 512:
                VIEW_Y = 512
            else:
                VIEW_Y = inW

    if outH <= VIEW_X:
        stepX = 1
    if outH > VIEW_X:
        stepX = outH / VIEW_X

    if outW <= VIEW_Y:
        stepY = 1
    if outW > VIEW_Y:
        stepY = outW / VIEW_Y

    window.geometry(str(int(VIEW_Y * 1.2)) + 'x' + str(int(VIEW_X * 1.2)))  # 벽
    canvas = Canvas(window, height=VIEW_X, width=VIEW_Y)
    paper = PhotoImage(height=VIEW_X, width=VIEW_Y)
    canvas.create_image((VIEW_Y // 2, VIEW_X // 2), image=paper, state='normal')

    import numpy
    # 성능 개선
    rgbStr = ""    # 전체 픽셀의 문자열을 저장
    for i in numpy.arange(0, outH, stepX):
        tmpStr = ""
        for k in numpy.arange(0, outW, stepY):
            i = int(i)
            k = int(k)
            r, g, b = outImage[R][i][k], outImage[G][i][k], outImage[B][i][k]
            tmpStr += " #%02x%02x%02x" % (r, g, b)    # 문자열에서 한 칸을 꼭 떼 줘야 나중에 자를 수 있다
        rgbStr += "{" + tmpStr + "} "     # 문자열에서 중괄호 끝에 한 칸을 꼭 떼 줘야 나중에 자를 수 있다
    paper.put(rgbStr)    # 문자열을 put하면 차례로 들어간다
    # 마우스 이벤트
    canvas.bind("<Button-1>", mouseClick)
    canvas.bind("<ButtonRelease-1>", mouseDrop)
    canvas.pack(expand=1, anchor=CENTER)
    status.configure(text = "이미지 정보: " + str(outW) + "x" + str(outH))

def saveImageColor():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW

    if outImage == None:
        return

    outArray = []
    for i in range(outH):
        tmpList = []
        for k in range(outW):
            tup = tuple([outImage[R][i][k], outImage[G][i][k], outImage[B][i][k]])
            tmpList.append(tup)
        outArray.append(tmpList)

    outArray = np.array(outArray)
    savePhoto = Image.fromarray(outArray.astype(np.uint8), "RGB")

    saveFp = asksaveasfile(parent=window, mode='wb', defaultextension=".",
                           filetypes=(("그림 파일", "*.png;*.jpg;*.bmp;*.tif"), ("모든 파일", "*.*")))
    if saveFp == "" or saveFp == None:
        return

    savePhoto.save(saveFp.name)
    print("Save.")





################################################
##### 컴퓨터 비전 (영상 처리) 알고리즘 함수 모음 #####
################################################

# 동일 영상
def equalImageColor():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정
    # 지금은 동일 영상이니까 크기 같음
    outH = inH
    outW = inW
    # 메모리 확보
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터비전 알고리즘
    outImage = inImage[:]
    displayImageColor()

# 밝게/어둡게 하기
def addminusImageColor():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    # 진짜 컴퓨터비전 알고리즘
    value = askinteger("밝게/어둡게 하기", "값 (-255 ~ 255)", minvalue = -255, maxvalue = 255)
    inImage = inImage.astype(np.int16)
    outImage = inImage + value
    outImage = np.where(outImage > 255, 255, outImage)
    outImage = np.where(outImage < 0, 0, outImage)
    displayImageColor()

# 화소값 반전
def reverseImageColor():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    outImage = 255 - inImage
    displayImageColor()

# 파라볼라
def paraImageColor():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    # 진짜 컴퓨터비전 알고리즘
    x = np.array([i for i in range(0, 256)])
    LUT = 255 - 255 * np.power(x / 128 - 1, 2)
    LUT = LUT.astype(np.uint8)
    outImage = LUT[inImage]
    displayImageColor()

# 모핑
def morphImageColor():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정
    outH = inH
    outW = inW
    # 추가 영상 선택
    filename2 = askopenfilename(parent=window,
                               filetypes=(("컬러 파일", "*.jpg;*.png;*.bmp;*.tif"), ("모든 파일", "*.*")))
    if filename2 == "" or filename2 == None:
        return

    inImage2 = []
    photo2 = Image.open(filename2)
    inH2 = photo2.height
    inW2 = photo2.width

    # 메모리 확보
    for _ in range(3):
        inImage2.append(malloc(inH2, inW2))

    photoRGB2 = photo2.convert("RGB")
    for i in range(inH2):
        for k in range(inW2):
            r, g, b = photoRGB2.getpixel((k, i))
            inImage2[R][i][k] = r
            inImage2[G][i][k] = g
            inImage2[B][i][k] = b

    ## 메모리 확보
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))

    import threading
    import time
    def morpFunc():
        w1 = 1;
        w2 = 0
        for _ in range(20):
            for RGB in range(3) :
                for i in range(inH):
                    for k in range(inW):
                        newValue = int(inImage[RGB][i][k] * w1 + inImage2[RGB][i][k] * w2)
                        if newValue > 255:
                            newValue = 255
                        elif newValue < 0:
                            newValue = 0
                        outImage[RGB][i][k] = newValue
            displayImageColor()
            w1 -= 0.05;
            w2 += 0.05
            time.sleep(0.5)

    threading.Thread(target=morpFunc).start()

# 이진화 알고리즘
def bwImageColor():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정
    outH = inH
    outW = inW
    # 크기 결정되었으니 메모리 할당
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))

    # 진짜 컴퓨터 비전 알고리즘이 여기부터 시작
    # grayscale로 변환
    avg_rgb = []
    avg_rgb = malloc(inH, inW)
    for i in range(inH):
        for k in range(inW):
            avg_rgb[i][k] = (inImage[R][i][k] + inImage[G][i][k] + inImage[B][i][k]) // 3

    # grayscale의 평균값 구하기
    sum = 0
    for i in range(inH):
        for k in range(inW):
            sum += avg_rgb[i][k]
    avg = sum // (inH*inW)

    # 평균값에 비교해 이진화
    for i in range(inH):
        for k in range(inW):
            if avg_rgb[i][k] < avg:
                outImage[R][i][k] = outImage[G][i][k] = outImage[B][i][k] = 0
            else:
                outImage[R][i][k] = outImage[G][i][k] = outImage[B][i][k] = 255

    displayImageColor()

# 영상 평균값 알고리즘
def avgImageColor():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    # 진짜 컴퓨터 비전 알고리즘이 여기부터 시작
    sum_r = 0
    for i in range(inH):
        for k in range(inW):
            sum_r += inImage[R][i][k]
    avg_r = sum_r / (inH*inW)
    sum_g = 0
    for i in range(inH):
        for k in range(inW):
            sum_g += inImage[G][i][k]
    avg_g = sum_g / (inH * inW)
    sum_b = 0
    for i in range(inH):
        for k in range(inW):
            sum_b += inImage[B][i][k]
    avg_b = sum_b / (inH * inW)
    messagebox.showinfo("평균값", "R 평균값: " + str(avg_r) + "\nG 평균값: " + str(avg_g) + "\nB 평균값: " + str(avg_b))

# 확대 (양선형 보간) 알고리즘
def upsizeImage2Color():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    v = askinteger("확대", "\"2\" 또는 \"4\" 또는 \"8\"만 입력", minvalue=2, maxvalue=8)
    # 중요! 출력 영상 크기 결정
    outH = inH * v
    outW = inW * v
    # 크기 결정되었으니 메모리 할당
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    # 진짜 컴퓨터 비전 알고리즘이 여기부터 시작
    rH, rW, iH, iW = [0] * 4    # 실수 위치 및 정수 위치
    x, y = 0, 0    # 실수와 정수의 차이값 (정수 위치로부터의 거리)
    C1, C2, C3, C4 = [0] * 4    # 결정할 위치 (N) 의 상하좌우 픽셀
    newValue = [0, 0, 0]
    for RGB in range(3):
        for i in range(outH):
            for k in range(outW):
                rH = i / v
                rW = k / v
                iH = int(rH)
                iW = int(rW)
                x = rW - iW
                y = rH - iH
                if 0 <= iH < inH-1 and 0<= iW < inW-1:
                    C1 = inImage[RGB][iH][iW]
                    C2 = inImage[RGB][iH][iW+1]
                    C3 = inImage[RGB][iH+1][iW+1]
                    C4 = inImage[RGB][iH+1][iW]
                    newValue[RGB] = C1 * (1-y) * (1-x) + C2 * (1-y) * x + C3 * y * x + C4 * y * (1-x)
                outImage[RGB][i][k] = int(newValue[RGB])
    displayImageColor()

# 축소 (평균 변환) 알고리즘
def downsizeImageColor():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    v = askinteger("축소", "\"2\" 또는 \"4\" 또는 \"8\"만 입력", minvalue=2, maxvalue=8)
    # 중요! 출력 영상 크기 결정
    outH = inH // v
    outW = inW // v
    # 크기 결정되었으니 메모리 할당
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    # 진짜 컴퓨터 비전 알고리즘이 여기부터 시작
    for RGB in range(3):
        for i in range(inH):
            for k in range(inW):
                outImage[RGB][i//v][k//v] += inImage[RGB][i][k]
        for i in range(outH):
            for k in range(outW):
                outImage[RGB][i][k] //= (v*v)
    displayImageColor()

# 히스토그램
import matplotlib.pyplot as plt
def histoImageColor():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    rCountList = [0] * 256
    gCountList = [0] * 256
    bCountList = [0] * 256
    tCountList = [0] * 256

    # grayscale로 변환 - R, G, B 평균값도 히스토그램에 표시하기 위해
    avg_rgb = []
    avg_rgb = malloc(inH, inW)
    for i in range(inH):
        for k in range(inW):
            avg_rgb[i][k] = (inImage[R][i][k] + inImage[G][i][k] + inImage[B][i][k]) // 3

    for i in range(inH):
        for k in range(inW):
            rCountList[inImage[R][i][k]] += 1
            gCountList[inImage[G][i][k]] += 1
            bCountList[inImage[B][i][k]] += 1
            tCountList[avg_rgb[i][k]] += 1
    plt.plot(rCountList, color="red")
    plt.plot(gCountList, color="green")
    plt.plot(bCountList, color="blue")
    plt.plot(tCountList, color="black")
    plt.show()

# 스트레칭(명암대비) 알고리즘
def stretchImageColor():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정
    # 지금은 동일 영상이니까 크기 같음
    outH = inH
    outW = inW
    # 크기 결정되었으니 메모리 할당
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))

    # 진짜 컴퓨터 비전 알고리즘이 여기부터 시작
    maxVal = [inImage[R][0][0], inImage[G][0][0], inImage[B][0][0]]
    minVal = [inImage[R][0][0], inImage[G][0][0], inImage[B][0][0]]

    for RGB in range(3):
        for i in range(inH):
            for k in range(inW):
                if inImage[RGB][i][k] < minVal[RGB]:
                    minVal[RGB] = inImage[RGB][i][k]
                elif inImage[RGB][i][k] > maxVal[RGB]:
                    maxVal[RGB] = inImage[RGB][i][k]

    for RGB in range(3):
        for i in range(inH):
            for k in range(inW):
                outImage[RGB][i][k] = int(((inImage[RGB][i][k] - minVal[RGB]) / (maxVal[RGB] - minVal[RGB])) * 255)

    displayImageColor()

# End-In 탐색 알고리즘
def endinImageColor():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정
    # 지금은 동일 영상이니까 크기 같음
    outH = inH
    outW = inW
    # 크기 결정되었으니 메모리 할당
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    # 진짜 컴퓨터 비전 알고리즘이 여기부터 시작
    maxVal = [inImage[R][0][0], inImage[G][0][0], inImage[B][0][0]]
    minVal = [inImage[R][0][0], inImage[G][0][0], inImage[B][0][0]]
    for RGB in range(3):
        for i in range(inH):
            for k in range(inW):
                if inImage[RGB][i][k] < minVal[RGB]:
                    minVal[RGB] = inImage[RGB][i][k]
                elif inImage[RGB][i][k] > maxVal[RGB]:
                    maxVal[RGB] = inImage[RGB][i][k]
    minAdd = askinteger("최소", "최소에서 추가 값", minvalue=0, maxvalue=255)
    maxAdd = askinteger("최대", "최대에서 감소 값", minvalue=0, maxvalue=255)
    for RGB in range(3):
        minVal[RGB] += minAdd
        maxVal[RGB] -= maxAdd
    for RGB in range(3):
        for i in range(inH):
            for k in range(inW):
                value = int(((inImage[RGB][i][k] - minVal[RGB]) / (maxVal[RGB] - minVal[RGB])) * 255)
                if value < 0:
                    value = 0
                elif value > 255:
                    value = 255
                outImage[RGB][i][k] = value
    displayImageColor()

# 히스토그램 평활화 알고리즘
def histoeqImageColor():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정
    # 지금은 동일 영상이니까 크기 같음
    outH = inH
    outW = inW
    # 크기 결정되었으니 메모리 할당
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))

    # 진짜 컴퓨터 비전 알고리즘이 여기부터 시작
    histo = [[0] * 256, [0] * 256, [0] * 256]
    sumHisto = [[0] * 256, [0] * 256, [0] * 256]
    normalHisto = [[0] * 256, [0] * 256, [0] * 256]
    sValue = [0, 0, 0]
    # 히스토그램
    for RGB in range(3):
        for i in range(inH):
            for k in range(inW):
                histo[RGB][inImage[RGB][i][k]] += 1
        # 누적 히스토그램
        for i in range(256):
            sValue[RGB] += histo[RGB][i]
            sumHisto[RGB][i] = sValue[RGB]
        # 정규화 누적 히스토그램
        for i in range(256):
            normalHisto[RGB][i] = int(sumHisto[RGB][i] / (inW*inH) * 255)
        # 영상 처리
        for i in range (inH):
            for k in range (inW):
                outImage[RGB][i][k] = normalHisto[RGB][inImage[RGB][i][k]]
    displayImageColor()

# 상하 반전 알고리즘
def updownImageColor():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정
    outH = inH
    outW = inW
    # 크기 결정되었으니 메모리 할당
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    # 진짜 컴퓨터 비전 알고리즘이 여기부터 시작
    for RGB in range(3):
        for i in range(inH):
            for k in range(inW):
                outImage[RGB][inH-i-1][k] = inImage[RGB][i][k]
    displayImageColor()

# 영상 이동 알고리즘 with 마우스
def moveImageColor():
    global panYN
    panYN = True
    canvas.configure(cursor = "mouse")    # 마우스가 활성화된걸 표시하도록 커서를 바꿈
def mouseClick(event):
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global sx, sy, ex, ey, panYN
    if panYN == False:
        return
    sx = event.x
    sy = event.y
def mouseDrop(event):
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global sx, sy, ex, ey, panYN
    if panYN == False:
        return
    ex = event.x
    ey = event.y
    # 중요! 출력 영상 크기 결정
    outH = inH
    outW = inW
    # 크기 결정되었으니 메모리 할당
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    # 진짜 컴퓨터 비전 알고리즘이 여기부터 시작
    mx = sx - ex    # x 이동량
    my = sy - ey    # y 이동량
    for RGB in range(3):
        for i in range(inH):
            for k in range(inW):
                if 0 <= i-my < outW and 0 <= k-mx < outH:    # 메모리 할당 범위 넘어가면 걍 패스되도록 if문 설정
                    outImage[RGB][i-my][k-mx] = inImage[RGB][i][k]
    panYN = False
    displayImageColor()

# 확대 알고리즘
def upsizeImageColor():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    v = askinteger("확대", "\"2\" 또는 \"4\" 또는 \"8\"만 입력", minvalue=2, maxvalue=8)
    # 중요! 출력 영상 크기 결정
    outH = inH * v
    outW = inW * v
    # 크기 결정되었으니 메모리 할당
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    # 진짜 컴퓨터 비전 알고리즘이 여기부터 시작
    for RGB in range(3):
        for i in range(outH):
            for k in range(outW):
                outImage[RGB][i][k] = inImage[RGB][i//v][k//v]    # backward 방식
    displayImageColor()

# 축소 알고리즘
def downsizeImage2Color():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    scale = askinteger("축소", "값 (\"2\" 또는 \"4\" 또는 \"8\"만 입력)", minvalue=2, maxvalue=8)
    # 중요! 출력 영상 크기 결정
    # 지금은 동일 영상이니까 크기 같음
    outH = inH // scale
    outW = inW // scale
    # 크기 결정되었으니 메모리 할당
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    for RGB in range(3):
        for i in range(outH):
            for k in range(outW):
                outImage[RGB][i][k] = inImage[RGB][i*scale][k*scale]
    displayImageColor()

# 회전2 알고리즘 - 중심, 역방향
def rotateImage2Color():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    angle = askinteger("회전", "각도 입력 (0~360)", minvalue=0, maxvalue=360)
    # 중요! 출력 영상 크기 결정
    # 지금은 동일 영상이니까 크기 같음
    outH = inH
    outW = inW
    # 크기 결정되었으니 메모리 할당
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    # 진짜 컴퓨터 비전 알고리즘이 여기부터 시작
    # angle(degree)를 라디안으로 바꾸기
    radian = (angle * math.pi) / 180
    cx = inW//2
    cy = inH//2
    for RGB in range(3):
        for i in range(outH):
            for k in range(outW):
                xs = i
                ys = k
                xd = int(math.cos(radian) * (xs-cx) - math.sin(radian) * (ys-cy)) + cx
                yd = int(math.sin(radian) * (xs-cx) + math.cos(radian) * (ys-cy)) + cy
                if 0 <= xd < inH and 0<= yd < inW:
                    outImage[RGB][xs][ys] = inImage[RGB][xd][yd]
                else:
                    outImage[RGB][xs][ys] = 255
    displayImageColor()

# 엠보싱 처리 알고리즘
def embossImageRGBColor():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정
    # 지금은 동일 영상이니까 크기 같음
    outH = inH
    outW = inW
    # 크기 결정되었으니 메모리 할당
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    # 진짜 컴퓨터 비전 알고리즘이 여기부터 시작
    MSIZE = 3
    mask = [[-1, 0, 0],
            [ 0, 0, 0],
            [ 0, 0, 1]]
    # 임시 입력 영상 메모리 확보
    tmpInImage = malloc(inH+(MSIZE-1), inW+(MSIZE-1), 127)
    tmpOutImage = malloc(outH, outW)
    # 원 입력 --> 임시 입력
    for RGB in range(3):
        for i in range(inH):
            for k in range(inW):
                tmpInImage[i+(MSIZE//2)][k+(MSIZE//2)] = inImage[RGB][i][k]
        # 회선 연산 (임시 입력 --> 임시 출력)
        for i in range((MSIZE//2), inH+(MSIZE//2)):
            for k in range((MSIZE//2), inW+(MSIZE//2)):
                # 각 점을 처리
                S = 0.0
                for m in range(0, MSIZE):
                    for n in range(0, MSIZE):
                        S += mask[m][n] * tmpInImage[i+m-(MSIZE//2)][k+n-(MSIZE//2)]
                tmpOutImage[i-(MSIZE//2)][k-(MSIZE//2)] = S
        # 127 더하기 (선택) -- 엠보싱 마스크를 씌우면서 영상이 전체적으로 어두워지는 효과를 보정하기 위해
        for i in range(outH):
            for k in range(outW):
                tmpOutImage[i][k] += 127
        # 임시 출력 --> 원 출력
        for i in range(outH):
            for k in range(outW):
                value = tmpOutImage[i][k]
                if value > 255:
                    value = 255
                elif value < 0:
                    value = 0
                outImage[RGB][i][k] = int(value)
    displayImageColor()

# 엠보싱 처리 알고리즘 (Pillow 이용)
def embossImagePILColor():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW, photo

    photo2 = photo.copy()
    photo2 = photo2.filter(ImageFilter.EMBOSS)

    # 지금은 크기 같음
    outH = inH
    outW = inW

    # 크기 결정되었으니 메모리 할당
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))

    for i in range(outH):
        for k in range(outW):
            r, g, b = photo2.getpixel((k, i))
            outImage[R][i][k] = r
            outImage[G][i][k] = g
            outImage[B][i][k] = b

    displayImageColor()

# 엠보싱 처리 알고리즘 (HSV 변환)
# RGB를 HSV로 변환 후 V만 마스크 처리 후 다시 합친 다음에 다시 RGB로 변환하는 작업
def embossImageHSVColor():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW, sx, sy, ex, ey

    # 이벤트 바인드
    canvas.bind("<Button-3>", rightMouseClick_embossImageHSVColor)
    canvas.bind("<Button-1>", leftMouseClick)
    canvas.bind("<B1-Motion>", leftMouseMove)
    canvas.bind("<ButtonRelease-1>", leftMouseDrop)
    canvas.configure(cursor="mouse")

def leftMouseClick(event):
    global sx, sy, ex, ey
    sx = event.x
    sy = event.y

boxLine = None
def leftMouseMove(event):
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW, sx, sy, ex, ey, boxLine
    ex = event.x
    ey = event.y
    if not boxLine:
        pass
    else:
        canvas.delete(boxLine)
    boxLine = canvas.create_rectangle(sx, sy, ex, ey, fill=None)

def leftMouseDrop(event):
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW, sx, sy, ex, ey

    ex = event.x - 1  # -1을 해야 제대로 된 범위가 구해진다
    ey = event.y - 1

    __embossImageHSVColor()

    canvas.unbind("<Button-3>")
    canvas.unbind("<Button-1>")
    canvas.unbind("<B1-Motion>")
    canvas.unbind("<ButtonRelease-1>")

def rightMouseClick_embossImageHSVColor(event):
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW, sx, sy, ex, ey
    sx = 0
    sy = 0
    ex = inW - 1    # -1을 해야 제대로 된 범위가 구해진다
    ey = inH - 1

    __embossImageHSVColor()

    canvas.unbind("<Button-3>")
    canvas.unbind("<Button-1>")
    canvas.unbind("<B1-Motion>")
    canvas.unbind("<ButtonRelease-1>")

def __embossImageHSVColor():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW

    ## 입력 RGB --> 입력 HSV
    # 메모리 확보
    inImageHSV = []
    for _ in range(3):
        inImageHSV.append(malloc(inH, inW))
    # RGB --> 입력 HSV
    for i in range(inH):
        for k in range(inW):
            r, g, b = inImage[R][i][k], inImage[G][i][k], inImage[B][i][k]
            h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
            inImageHSV[0][i][k], inImageHSV[1][i][k], inImageHSV[2][i][k] = h, s, v

    # 지금은 크기 같음
    outH = inH
    outW = inW
    # 크기 결정되었으니 메모리 할당
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))

    ## 진짜 컴퓨터 비전 알고리즘이 여기부터 시작
    MSIZE = 3
    mask = [[-1, 0, 0],
            [ 0, 0, 0],
            [ 0, 0, 1]]

    # 임시 입력 영상 메모리 확보
    tmpInImage = malloc(inH+(MSIZE-1), inW+(MSIZE-1), 127)
    tmpOutImage = malloc(outH, outW)

    # 원 입력 --> 임시 입력
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i+(MSIZE//2)][k+(MSIZE//2)] = inImageHSV[2][i][k]

    # 회선 연산 (임시 입력 --> 임시 출력)
    for i in range((MSIZE//2), inH+(MSIZE//2)):
        for k in range((MSIZE//2), inW+(MSIZE//2)):
            # 각 점을 처리
            S = 0.0
            for m in range(0, MSIZE):
                for n in range(0, MSIZE):
                    S += mask[m][n] * tmpInImage[i+m-(MSIZE//2)][k+n-(MSIZE//2)]
            tmpOutImage[i-(MSIZE//2)][k-(MSIZE//2)] = S * 255

    # 127 더하기 (선택) -- 엠보싱 마스크를 씌우면서 영상이 전체적으로 어두워지는 효과를 보정하기 위해
    for i in range(outH):
        for k in range(outW):
            tmpOutImage[i][k] += 127
            if tmpOutImage[i][k] > 255:
                tmpOutImage[i][k] = 255
            elif tmpOutImage[i][k] < 0:
                tmpOutImage[i][k] = 0

    # HSV --> RGB
    for i in range(outH):
        for k in range(outW):
            if sx <= k <= ex and sy <= i <= ey:
                h, s, v = inImageHSV[0][i][k], inImageHSV[1][i][k], tmpOutImage[i][k]
                r, g, b = colorsys.hsv_to_rgb(h, s, v)
                outImage[R][i][k], outImage[G][i][k], outImage[B][i][k] = int(r), int(g), int(b)
            else:
                outImage[R][i][k], outImage[G][i][k], outImage[B][i][k] = inImage[R][i][k], inImage[G][i][k], inImage[B][i][k]

    displayImageColor()

# 블러 처리 알고리즘
def blurImageRGBColor():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정
    # 지금은 동일 영상이니까 크기 같음
    outH = inH
    outW = inW
    # 크기 결정되었으니 메모리 할당
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    # 진짜 컴퓨터 비전 알고리즘이 여기부터 시작
    MSIZE = 3
    mask = [[1/9, 1/9, 1/9],
            [1/9, 1/9, 1/9],
            [1/9, 1/9, 1/9]]
    # 임시 입력 영상 메모리 확보
    tmpInImage = malloc(inH+(MSIZE-1), inW+(MSIZE-1), 127)
    tmpOutImage = malloc(outH, outW)
    # 원 입력 --> 임시 입력
    for RGB in range(3):
        for i in range(inH):
            for k in range(inW):
                tmpInImage[i+(MSIZE//2)][k+(MSIZE//2)] = inImage[RGB][i][k]
        # 회선 연산 (임시 입력 --> 임시 출력)
        for i in range((MSIZE//2), inH+(MSIZE//2)):
            for k in range((MSIZE//2), inW+(MSIZE//2)):
                # 각 점을 처리
                S = 0.0
                for m in range(0, MSIZE):
                    for n in range(0, MSIZE):
                        S += mask[m][n] * tmpInImage[i+m-(MSIZE//2)][k+n-(MSIZE//2)]
                tmpOutImage[i-(MSIZE//2)][k-(MSIZE//2)] = S
        # 임시 출력 --> 원 출력
        for i in range(outH):
            for k in range(outW):
                value = tmpOutImage[i][k]
                if value > 255:
                    value = 255
                elif value < 0:
                    value = 0
                outImage[RGB][i][k] = int(value)
    displayImageColor()

# 채도 조절 알고리즘 (Pillow 이용)
def addSValuePillow():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW, photo

    value = askfloat("채도 조절", "0 ~ 1 ~ 10")
    photo2 = photo.copy()
    photo2 = ImageEnhance.Color(photo2)
    photo2 = photo2.enhance(value)

    # 지금은 크기 같음
    outH = inH
    outW = inW

    # 크기 결정되었으니 메모리 할당
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))

    for i in range(outH):
        for k in range(outW):
            r, g, b = photo2.getpixel((k, i))
            outImage[R][i][k] = r
            outImage[G][i][k] = g
            outImage[B][i][k] = b

    displayImageColor()

# 채도 조절 알고리즘 (HSV 이용)
def addSValueHSV():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW

    ## 입력 RGB --> 입력 HSV
    # 메모리 확보
    inImageHSV = []
    for _ in range(3):
        inImageHSV.append(malloc(inH, inW))
    # RGB --> 입력 HSV
    for i in range(inH):
        for k in range(inW):
            r, g, b = inImage[R][i][k], inImage[G][i][k], inImage[B][i][k]
            h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            inImageHSV[0][i][k], inImageHSV[1][i][k], inImageHSV[2][i][k] = h, s, v

    # 지금은 크기 같음
    outH = inH
    outW = inW
    # 크기 결정되었으니 메모리 할당
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))

    ## 진짜 컴퓨터 비전 알고리즘이 여기부터 시작

    value = askfloat("채도 조절", "-255 ~ 255")
    value /= 255

    # HSV --> RGB
    for i in range(outH):
        for k in range(outW):
            newS = inImageHSV[1][i][k] + value
            if newS < 0:
                newS = 0
            elif newS > 1.0:
                newS = 1.0
            h, s, v = inImageHSV[0][i][k], newS, inImageHSV[2][i][k] * 255 # 명도에는 255를 곱해줘야 한다
            r, g, b = colorsys.hsv_to_rgb(h, s, v)
            outImage[R][i][k], outImage[G][i][k], outImage[B][i][k] = int(r), int(g), int(b)

    displayImageColor()

# 임시 경로에 outImage를 저장하기
import random
def saveTempImage():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    import tempfile
    saveFp = tempfile.gettempdir() + "/" + os.path.basename(filename)
    if saveFp == "" or saveFp == None:
        return
    saveFp = open(saveFp, mode="wb")

    outArray = []
    for i in range(outH):
        tmpList = []
        for k in range(outW):
            tup = tuple([outImage[R][i][k], outImage[G][i][k], outImage[B][i][k]])
            tmpList.append(tup)
        outArray.append(tmpList)

    outArray = np.array(outArray)
    savePhoto = Image.fromarray(outArray.astype(np.uint8), "RGB")

    savePhoto.save(saveFp.name)
    saveFp.close()
    return saveFp

# MySQL에 저장
def saveMysqlColor():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW

    con = pymysql.connect(host=IP_ADDR, user=USER_NAME, password=USER_PW, db=DB_NAME, charset=CHAR_SET)
    cur = con.cursor()

    try:
        sql = "CREATE TABLE colorImage_TBL (raw_id INT AUTO_INCREMENT PRIMARY KEY, raw_fname VARCHAR(30), raw_extname CHAR(5), raw_height SMALLINT, raw_width SMALLINT, raw_data LONGBLOB);"
        cur.execute(sql)
    except:
        pass

    # outImage를 임시 폴더에 저장하고, 이걸 fullname으로 전달

    fullname = saveTempImage()
    fullname = fullname.name

    with open(fullname, "rb") as rfp:    # rb = read binary
        binData = rfp.read()

    fname, extname = os.path.basename(fullname).split(".")
    photo = Image.open(fullname)
    height = photo.height
    width = photo.width

    # avgVal, maxVal, minVal = findStat(fullname)    # 평균, 최대, 최소

    sql = "INSERT INTO colorimage_tbl (raw_id, raw_fname, raw_extname, raw_height, raw_width, raw_data)"
    sql += " VALUES(NULL, '" + fname + "', '" + extname + "', " + str(height) + ", " + str(width) + ", %s)"

    tupleData = (binData,)
    cur.execute(sql, tupleData)
    con.commit()
    cur.close()
    con.close()

    print("끝!!")

# MySQL에서 불러오기
def loadMysqlColor():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW

    con = pymysql.connect(host=IP_ADDR, user=USER_NAME, password=USER_PW, db=DB_NAME, charset=CHAR_SET)
    cur = con.cursor()

    sql = "SELECT raw_id, raw_fname, raw_extname, raw_height, raw_width FROM colorimage_tbl"
    cur.execute(sql)

    queryList = cur.fetchall()
    rowList = [":".join(map(str,row)) for row in queryList]

    def selectRecord():
        global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
        selIndex = listbox.curselection()[0]
        subWindow.destroy()
        raw_id = queryList[selIndex][0]
        sql = "SELECT raw_fname, raw_extname, raw_data FROM colorimage_tbl WHERE raw_id = " + str(raw_id)
        cur.execute(sql)
        fname, extname, binData = cur.fetchone()
        import tempfile
        # 모든 windows 컴퓨터에 있는 temp 폴더에 저장하기
        fullPath = tempfile.gettempdir() + "/" + fname + "." + extname
        with open(fullPath, "wb") as wfp:  # wb = write binary
            wfp.write(binData)
        cur.close()
        con.close()

        loadImageColor(fullPath)
        equalImageColor()
        os.remove(fullPath)

    # 서브 윈도우에 목록 출력하기
    subWindow = Toplevel(window)    # Toplevel(window) = "window라는 Tk 밑에 있는 새로운 Tk이다"라는 뜻
    # subWindow.geometry("256x256")
    listbox = Listbox(subWindow)
    button = Button(subWindow, text="선택", command = selectRecord)
    for rowStr in rowList:
        listbox.insert(END, rowStr)

    listbox.pack(expand=1, anchor=CENTER)
    button.pack()
    subWindow.mainloop()

    cur.close()
    con.close()

# CSV 파일 불러오기
def loadCsvColor(fname):
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    with open(fname, "r") as rFp:  # rb = binary
        for row_list in rFp:
            row, col = list(map(int,row_list.strip().split(",")))[0:2]
            inH = row + 1
            inW = col + 1
    inImage = []
    for _ in range(3):
        inImage.append(malloc(inH, inW))
    # 파일에서 메모리로 가져오기
    with open(fname, "r") as rFp:  # rb = binary
        for row_list in rFp:
            row, col, r, g, b = list(map(int,row_list.strip().split(",")))
            inImage[R][row][col], inImage[G][row][col], inImage[B][row][col] = r, g, b

# CSV 파일을 선택해서 메모리로 로딩하는 함수
def openCsvColor():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH,outW
    filename = askopenfilename(parent=window,
                               filetypes=(("CSV 파일", "*.csv"), ("모든 파일", "*.*")))
    if filename == "" or filename == None:
        return
    loadCsvColor(filename)
    equalImageColor()

# CSV 파일로 저장하기
def saveCsvColor():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    saveFp = asksaveasfile(parent=window, mode='wb', defaultextension="*.csv", filetypes=(("CSV 파일", "*.csv"), ("모든 파일", "*.*")))
    if saveFp == "" or saveFp == None:
        return
    with open(saveFp.name, mode="w", newline="") as wFp:
        csvWriter = csv.writer(wFp)
        for i in range (outH):
            for k in range (outW):
                row_list = [i, k, outImage[R][i][k], outImage[G][i][k], outImage[B][i][k]]
                csvWriter.writerow(row_list)
    print("CSV. save OK")

# 엑셀아트로 저장하기
def saveExcelArtColor():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    saveFp = asksaveasfile(parent=window, mode='wb', defaultextension="*.xls", filetypes=(("XLS 파일", "*.xls"), ("모든 파일", "*.*")))
    if saveFp == "" or saveFp == None:
        return
    xlsName = saveFp.name
    sheetName = os.path.basename(filename)

    wb = xlsxwriter.Workbook(xlsName)
    ws = wb.add_worksheet(sheetName)

    ws.set_column(0, outW-1, 1.0)    # 약 0.34
    # 폭은 한번에 조절되지만 높이는 하나씩 조절해야 한다
    for i in range(outH):
        ws.set_row(i, 9.5)    # 약 0.35

    for i in range(outH):
        for k in range(outW):
            hexStr = [0] * 3
            for RGB in range(3):
                data = outImage[RGB][i][k]
                # data 값으로 셀의 배경색을 조절 #000000 ~ #FFFFFF
                if data>15:
                    hexStr[RGB] = hex(data)[2:]
                else:    # 15 미만은 한자리수가 되므로 앞에 0을 붙여줘야 3을 곱했을 때 6자리가 된다
                    hexStr[RGB] = ("0" + hex(data)[2:])
            # 셀의 포맷을 준비
            cell_format = wb.add_format()
            cell_format.set_bg_color("#" + str(hexStr[R]) + str(hexStr[G]) + str(hexStr[B]))
            ws.write(i, k, "", cell_format)
    wb.close()
    print("Excel Art. save OK")

# 엑셀로 저장하기 -- 가로길이 256 이하만 저장 가능
def saveExcelColor():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    saveFp = asksaveasfile(parent=window, mode='wb', defaultextension="*.xls", filetypes=(("XLS 파일", "*.xls"), ("모든 파일", "*.*")))
    if saveFp == "" or saveFp == None:
        return
    xlsName = saveFp.name
    sheetName = os.path.basename(filename)
    wb = xlwt.Workbook()
    ws_r = wb.add_sheet(sheetName + "_R")
    ws_g = wb.add_sheet(sheetName + "_G")
    ws_b = wb.add_sheet(sheetName + "_B")
    for i in range(outH):
        for k in range(outW):
            ws_r.write(i, k, outImage[R][i][k])
            ws_g.write(i, k, outImage[G][i][k])
            ws_b.write(i, k, outImage[B][i][k])
    wb.save(xlsName)
    print("Excel. save OK")

# 엑셀에서 불러오기
def loadExcelColor(fname):
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW

    wb = xlrd.open_workbook(fname)
    ws = wb.sheets()

    inH = ws[0].nrows
    inW = ws[0].ncols

    inImage = []
    for _ in range(3):
        inImage.append(malloc(inH, inW))

    for RGB in range(3):
        for i in range(inH):
            for k in range(inW):
                inImage[RGB][i][k] = int(ws[RGB].cell_value(i, k))

def openExcelColor():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH,outW
    filename = askopenfilename(parent=window,
                               filetypes=(("엑셀 파일", "*.xls;*.xlsx"), ("모든 파일", "*.*")))
    if filename == "" or filename == None:
        return
    loadExcelColor(filename)
    equalImageColor()





##########################
##### 전역 변수 선언부 #####
##########################

R, G, B = 0, 1, 2
inImage, outImage = [], []    # 3차원 배열
inH, inW, outH, outW, dispW, dispH = [0] * 6

window, canvas, paper = None, None, None
filename = ""

VIEW_X, VIEW_Y = 512, 512 # 화면에 보일 크기 (출력용)

panYN = False
sx, sy, ex, ey = [0] * 4

IP_ADDR = "192.168.56.112"
USER_NAME = "root"
USER_PW = "1234"
DB_NAME = "BigData_DB"
CHAR_SET = "utf8"





#####################
##### 메인 코드부 #####
#####################

window = Tk()
window.geometry("500x500")
window.title("컴퓨터 비전 (딥러닝 - 컬러) Ver 0.01")

status = Label(window, text = "이미지 정보: ", bd = 1, relief = SUNKEN, anchor = W)
status.pack(side=BOTTOM, fill=X)



mainMenu = Menu(window)
window.config(menu=mainMenu)

fileMenu = Menu(mainMenu)
mainMenu.add_cascade(label="파일", menu=fileMenu)
fileMenu.add_command(label="파일 열기", command=openImageColor)
fileMenu.add_separator()
fileMenu.add_command(label="파일 저장", command=saveImageColor)

comVisionMenu1 = Menu(mainMenu)
mainMenu.add_cascade(label="화소점 처리", menu=comVisionMenu1)
comVisionMenu1.add_command(label="밝게/어둡게 하기", command=addminusImageColor)
comVisionMenu1.add_command(label="화소값 반전", command=reverseImageColor)
comVisionMenu1.add_command(label="파라볼라", command=paraImageColor)
comVisionMenu1.add_separator()
comVisionMenu1.add_command(label="모핑", command=morphImageColor)
comVisionMenu1.add_command(label="채도 조절 (Pillow)", command=addSValuePillow)
comVisionMenu1.add_command(label="채도 조절 (HSV)", command=addSValueHSV)

comVisionMenu2 = Menu(mainMenu)
mainMenu.add_cascade(label="화소 (통계)", menu=comVisionMenu2)
comVisionMenu2.add_command(label="이진화 (= 흑백)", command=bwImageColor)
comVisionMenu2.add_command(label="입력/출력 영상 평균값", command=avgImageColor)
comVisionMenu2.add_command(label="확대 (양선형 보간)", command=upsizeImage2Color)
comVisionMenu2.add_command(label="축소 (평균 변환)", command=downsizeImageColor)
comVisionMenu2.add_separator()
comVisionMenu2.add_command(label="히스토그램", command=histoImageColor)
# comVisionMenu2.add_command(label="히스토그램 (시각화 연습)", command=histoImage2)
comVisionMenu2.add_command(label="명암대비", command=stretchImageColor)
comVisionMenu2.add_command(label="End-In 탐색", command=endinImageColor)
comVisionMenu2.add_command(label="히스토그램 평활화", command=histoeqImageColor)

comVisionMenu3 = Menu(mainMenu)
mainMenu.add_cascade(label="기하학 처리", menu=comVisionMenu3)
comVisionMenu3.add_command(label="상하 반전", command=updownImageColor)
comVisionMenu3.add_command(label="이동 (상하/좌우)", command=moveImageColor)
comVisionMenu3.add_command(label="확대", command=upsizeImageColor)
comVisionMenu3.add_command(label="축소", command=downsizeImage2Color)
# comVisionMenu3.add_command(label="오른쪽 90도 회전", command=clock90Image)
# comVisionMenu3.add_command(label="회전", command=rotateImage)
comVisionMenu3.add_command(label="회전2 (중심, 역방향)", command=rotateImage2Color)

comVisionMenu4 = Menu(mainMenu)
mainMenu.add_cascade(label="화소 영역 처리", menu=comVisionMenu4)
comVisionMenu4.add_command(label="엠보싱 처리 (RGB)", command=embossImageRGBColor)
comVisionMenu4.add_command(label="엠보싱 처리 (Pillow 제공)", command=embossImagePILColor)
comVisionMenu4.add_command(label="엠보싱 처리 (HSV)", command=embossImageHSVColor)
comVisionMenu4.add_command(label="블러 처리", command=blurImageRGBColor)
# comVisionMenu4.add_command(label="샤프닝 처리", command=sharpenImage)
# comVisionMenu4.add_command(label="가우시안 필터링", command=gaussImage)
# comVisionMenu4.add_command(label="고주파 필터 샤프닝", command=hpfsharpenImage)
# comVisionMenu4.add_command(label="저주파 필터 샤프닝", command=lpfsharpenImage)
# comVisionMenu4.add_command(label="경계선 검출", command=edgeImage)

comVisionMenu5 = Menu(mainMenu)
mainMenu.add_cascade(label="기타 입출력", menu=comVisionMenu5)
comVisionMenu5.add_command(label="MySQL에서 불러오기", command=loadMysqlColor)
comVisionMenu5.add_command(label="MySQL로 저장하기", command=saveMysqlColor)
comVisionMenu2.add_separator()
comVisionMenu5.add_command(label="CSV 열기", command=openCsvColor)
comVisionMenu5.add_command(label="CSV 저장", command=saveCsvColor)
comVisionMenu2.add_separator()
comVisionMenu5.add_command(label="엑셀 열기", command=openExcelColor)
comVisionMenu5.add_command(label="엑셀 저장", command=saveExcelColor)
comVisionMenu5.add_command(label="엑셀 아트로 저장", command=saveExcelArtColor)



window.mainloop()