from tkinter import *
from tkinter.simpledialog import *
from tkinter.filedialog import *
import math
import os
import os.path
import struct



#####################
##### 함수 선언부 #####
#####################

# 메모리를 할당해서 리스트(참조)를 반환하는 함수
def malloc(h, w, initValue=0):    # malloc = memory allocate
    retMemory = []
    for _ in range (h):
        tmpList = []
        for _ in range (w):
            tmpList.append(initValue)
        retMemory.append(tmpList)
    return retMemory

# 파일을 메모리로 로딩하는 함수
def loadImage(fname):
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    fsize = os.path.getsize(fname)    # 파일의 크기 (바이트)
    inH = inW = int(math.sqrt(fsize))    # 핵심 코드
    # 입력 영상 메모리 확보
    inImage = []
    inImage = malloc(inH, inW)
    # 파일에서 메모리로 가져오기
    with open(filename, "rb") as rFp:  # rb = binary
        for i in range (inH):
            for k in range (inW):
                inImage[i][k] = int(ord(rFp.read(1)))

# 파일을 선택해서 메모리로 로딩하는 함수
def openImage():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH,outW
    filename = askopenfilename(parent=window,
                               filetypes=(("RAW 파일", "*.raw"), ("모든 파일", "*.*")))
    if filename == "" or filename == None:
        return
    loadImage(filename)
    equalImage()

def saveImage():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    saveFp = asksaveasfile(parent=window, mode='wb', defaultextension="*.raw", filetypes=(("RAW 파일", "*.raw"), ("모든 파일", "*.*")))
    if saveFp == "" or saveFp == None:
        return
    for i in range (outH):
        for k in range (outW):
            saveFp.write(struct.pack("B", outImage[i][k]))
    saveFp.close()

# ## 8일차 미션1 선택1 내 풀이 ##
# def displayImage():
#     global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW, dispW, dispH
#     if canvas!= None:    # 예전에 실행한 적이 있다면
#         canvas.destroy()
#     # 화면 크기를 조절
#     dispH = outH
#     dispW = outW
#     if outH > 512:
#         dispW //= (outH/512)
#         dispH = 512
#     elif outW > 512:
#         dispH //= (outW/512)
#         dispW = 512
#     dispH = int(dispH)
#     dispW = int(dispW)
#
#     if (outH <= 512) and (outW <= 512):
#         window.geometry(str(outH) + "x" + str(outW))  # 벽
#         canvas = Canvas(window, height=outH, width=outW)  # 보드
#         paper = PhotoImage(height=outH, width=outW)  # 빈 종이
#         canvas.create_image((outH // 2, outW // 2), image=paper, state="normal")
#         rgbStr = ""  # 전체 픽셀의 문자열을 저장
#         for i in range(outH):
#             tmpStr = ""
#             for k in range(outW):
#                 r = g = b = outImage[i][k]
#                 tmpStr += " #%02x%02x%02x" % (r, g, b)  # 문자열에서 한 칸을 꼭 떼 줘야 나중에 자를 수 있다
#             rgbStr += "{" + tmpStr + "} "  # 문자열에서 중괄호 끝에 한 칸을 꼭 떼 줘야 나중에 자를 수 있다
#         paper.put(rgbStr)  # 문자열을 put하면 차례로 들어간다
#     else:
#         window.geometry(str(dispH) + "x" + str(dispW))  # 벽
#         canvas = Canvas(window, height=dispH, width=dispW)  # 보드
#         paper = PhotoImage(height=dispH, width=dispW)  # 빈 종이
#         canvas.create_image((dispH // 2, dispW // 2), image=paper, state="normal")
#         rgbStr = ""  # 전체 픽셀의 문자열을 저장
#         for i in range(dispH):
#             tmpStr = ""
#             for k in range(dispW):
#                 r = g = b = outImage[i*(outH//dispH)][k*(outH//dispH)]
#                 tmpStr += " #%02x%02x%02x" % (r, g, b)  # 문자열에서 한 칸을 꼭 떼 줘야 나중에 자를 수 있다
#             rgbStr += "{" + tmpStr + "} "  # 문자열에서 중괄호 끝에 한 칸을 꼭 떼 줘야 나중에 자를 수 있다
#         paper.put(rgbStr)  # 문자열을 put하면 차례로 들어간다
#
#     # 마우스 이벤트
#     canvas.bind("<Button-1>", mouseClick)
#     canvas.bind("<ButtonRelease-1>", mouseDrop)
#     canvas.pack(expand=1, anchor=CENTER)

def displayImage():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global VIEW_X, VIEW_Y
    if canvas!= None:    # 예전에 실행한 적이 있다면
        canvas.destroy()
    # # 화면 크기를 조절
    # window.geometry(str(outH)+"x"+str(outW))    # 벽
    # canvas = Canvas(window, height = outH, width = outW)    # 보드
    # paper = PhotoImage(height = outH, width = outW)    # 빈 종이
    # canvas.create_image((outH//2, outW//2), image = paper, state = "normal")
    # 고정된 화면 크기
    if outH <= VIEW_Y or outW <= VIEW_X:
        VIEW_X = outW
        VIEW_Y = outH
        step = 1
    else:
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
    # 마우스 이벤트
    canvas.bind("<Button-1>", mouseClick)
    canvas.bind("<ButtonRelease-1>", mouseDrop)
    canvas.pack(expand=1, anchor=CENTER)
    # 이미지 정보
    status.configure(text = "이미지 정보: " + str(outW) + "x" + str(outH))



################################################
##### 컴퓨터 비전 (영상 처리) 알고리즘 함수 모음 #####
################################################

# 동일 영상 알고리즘
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

# 밝게/어둡게 하기 알고리즘
def addminusImage():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정
    outH = inH
    outW = inW
    # 크기 결정되었으니 메모리 할당
    outImage = []
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘이 여기부터 시작
    value = askinteger("밝게/어둡게 하기", "값 (-255 ~ 255)", minvalue = -255, maxvalue = 255)
    for i in range(inH):
        for k in range(inW):
            v = inImage[i][k] + value
            if v > 255:
                v = 255
            elif v < 0:
                v = 0
            outImage[i][k] = v
    displayImage()

# 영상 곱셈 알고리즘
def multiplyImage():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정
    outH = inH
    outW = inW
    # 크기 결정되었으니 메모리 할당
    outImage = []
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘이 여기부터 시작
    value = askinteger("영상 곱셈", "곱할 값", minvalue = 1, maxvalue = 255)
    for i in range(inH):
        for k in range(inW):
            outImage[i][k] = inImage[i][k] * value
            if outImage[i][k] > 255:
                outImage[i][k] = 255
    displayImage()

# 영상 나눗셈 알고리즘
def divideImage():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정
    outH = inH
    outW = inW
    # 크기 결정되었으니 메모리 할당
    outImage = []
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘이 여기부터 시작
    value = askinteger("영상 나눗셈", "나눌 값", minvalue = 1, maxvalue = 255)
    for i in range(inH):
        for k in range(inW):
            outImage[i][k] = inImage[i][k] // value
            if outImage[i][k] < 0:
                outImage[i][k] = 0
    displayImage()

# 화소값 반전 알고리즘
def reverseImage():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정
    outH = inH
    outW = inW
    # 크기 결정되었으니 메모리 할당
    outImage = []
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘이 여기부터 시작
    for i in range(inH):
        for k in range(inW):
            outImage[i][k] = 255 - inImage[i][k]
            if outImage[i][k] < 0:
                outImage[i][k] = 0
            elif outImage[i][k] > 255:
                outImage[i][k] = 255
    displayImage()

# 이진화 알고리즘
def bwImage():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정
    outH = inH
    outW = inW
    # 크기 결정되었으니 메모리 할당
    outImage = []
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘이 여기부터 시작
    # 영상의 평균 구하기
    sum = 0
    for i in range(inH):
        for k in range(inW):
            sum += inImage[i][k]
    avg = sum // (inH*inW)
    for i in range(inH):
        for k in range(inW):
            if inImage[i][k] < avg:
                outImage[i][k] = 0
            else:
                outImage[i][k] = 255
    displayImage()

# 영상 평균값 알고리즘
def avgImage():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    # 진짜 컴퓨터 비전 알고리즘이 여기부터 시작
    sum = 0
    for i in range(inH):
        for k in range(inW):
            sum += inImage[i][k]
    avg = sum / (inH*inW)
    messagebox.showinfo("평균값", avg)

# Posterization 알고리즘
def posterizeImage():
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
            if outImage[i][k] < 0:
                outImage[i][k] = 0
            elif outImage[i][k] < 50:
                outImage[i][k] = 25
            elif outImage[i][k] < 100:
                outImage[i][k] = 75
            elif outImage[i][k] < 150:
                outImage[i][k] = 125
            elif outImage[i][k] < 200:
                outImage[i][k] = 175
            elif outImage[i][k] < 255:
                outImage[i][k] = 225
            else:
                outImage[i][k] = 255
    displayImage()

# # 파라볼라 알고리즘
# def paraImage():
#     global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
#     # 중요! 출력 영상 크기 결정
#     outH = inH
#     outW = inW
#     # 크기 결정되었으니 메모리 할당
#     outImage = []
#     outImage = malloc(outH, outW)
#     # 진짜 컴퓨터 비전 알고리즘이 여기부터 시작
#     for i in range(inH):
#         for k in range(inW):
#             input = inImage[i][k]
#             outImage[i][k] = int(255 - 255 * math.pow(input/128 - 1, 2))
#     displayImage()

# 파라볼라 알고리즘 with LUT (Look Up Table)
def paraImage():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정
    outH = inH
    outW = inW
    # 크기 결정되었으니 메모리 할당
    outImage = []
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘이 여기부터 시작
    LUT = [0 for _ in range(256)]
    for input in range(256):
        LUT[input] = int(255 - 255 * math.pow(input/128 - 1, 2))
    for i in range(inH):
        for k in range(inW):
            outImage[i][k] = LUT[inImage[i][k]]
    displayImage()

# 상하 반전 알고리즘
def updownImage():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정
    outH = inH
    outW = inW
    # 크기 결정되었으니 메모리 할당
    outImage = []
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘이 여기부터 시작
    for i in range(inH):
        for k in range(inW):
            outImage[inH-i-1][k] = inImage[i][k]
    displayImage()

# # 영상 이동 알고리즘
# def moveImage():
#     global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
#     # 중요! 출력 영상 크기 결정
#     # 지금은 동일 영상이니까 크기 같음
#     outH = inH
#     outW = inW
#     # 크기 결정되었으니 메모리 할당
#     outImage = []
#     outImage = malloc(outH, outW)
#     # 진짜 컴퓨터 비전 알고리즘이 여기부터 시작
#     vH = askinteger("영상 이동", "상하 (-는 위로 +는 아래로)", minvalue=-inH, maxvalue=inH)
#     vW = askinteger("영상 이동", "좌우 (-는 왼쪽으로 +는 오른쪽으로)", minvalue=-inW, maxvalue=inW)
#     for i in range(inH):
#         ni = 0
#         ni = i + vH
#         if ni >= inH:
#             ni -= inH
#         elif ni < 0:
#             ni += inH
#         for k in range(inW):
#             nk = 0
#             nk = k + vW
#             if nk >= inW:
#                 nk -= inW
#             elif nk < 0:
#                 nk += inW
#             outImage[ni][nk] = inImage[i][k]
#     displayImage()

# 영상 이동 알고리즘 with 마우스
def moveImage():
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
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘이 여기부터 시작
    mx = sx - ex    # x 이동량
    my = sy - ey    # y 이동량
    for i in range(inH):
        for k in range(inW):
            if 0 <= i-my < outW and 0 <= k-mx < outH:    # 메모리 할당 범위 넘어가면 걍 패스되도록 if문 설정
                outImage[i-my][k-mx] = inImage[i][k]
    panYN = False
    displayImage()

# # 확대 알고리즘
# def upsizeImage():
#     global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
#     v = askinteger("확대", "\"2\" 또는 \"4\"만 입력", minvalue=2, maxvalue=4)
#     # 중요! 출력 영상 크기 결정
#     outH = inH * v
#     outW = inW * v
#     # 크기 결정되었으니 메모리 할당
#     outImage = []
#     outImage = malloc(outH, outW)
#     # 진짜 컴퓨터 비전 알고리즘이 여기부터 시작
#     for i in range(inH):
#         for k in range(inW):
#             for l in range(v):
#                 for m in range(v):
#                     outImage[i * v + l][k * v + m] = inImage[i][k]
#     displayImage()

# 확대 알고리즘
def upsizeImage():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    v = askinteger("확대", "\"2\" 또는 \"4\" 또는 \"8\"만 입력", minvalue=2, maxvalue=8)
    # 중요! 출력 영상 크기 결정
    outH = inH * v
    outW = inW * v
    # 크기 결정되었으니 메모리 할당
    outImage = []
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘이 여기부터 시작
    for i in range(outH):
        for k in range(outW):
            outImage[i][k] = inImage[i//v][k//v]    # backward 방식
    displayImage()

# 확대 (양선형 보간) 알고리즘
def upsizeImage2():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    v = askinteger("확대", "\"2\" 또는 \"4\" 또는 \"8\"만 입력", minvalue=2, maxvalue=8)
    # 중요! 출력 영상 크기 결정
    outH = inH * v
    outW = inW * v
    # 크기 결정되었으니 메모리 할당
    outImage = []
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘이 여기부터 시작
    rH, rW, iH, iW = [0] * 4    # 실수 위치 및 정수 위치
    x, y = 0, 0    # 실수와 정수의 차이값 (정수 위치로부터의 거리)
    C1, C2, C3, C4 = [0] * 4    # 결정할 위치 (N) 의 상하좌우 픽셀
    for i in range(outH):
        for k in range(outW):
            rH = i / v
            rW = k / v
            iH = int(rH)
            iW = int(rW)
            x = rW - iW
            y = rH - iH
            if 0 <= iH < inH-1 and 0<= iW < inW-1:
                C1 = inImage[iH][iW]
                C2 = inImage[iH][iW+1]
                C3 = inImage[iH+1][iW+1]
                C4 = inImage[iH+1][iW]
                newValue = C1 * (1-y) * (1-x) + C2 * (1-y) * x + C3 * y * x + C4 * y * (1-x)
            outImage[i][k] = int(newValue)
    displayImage()

# # 축소 (평균 변환) 알고리즘
# def downsizeImage():
#     global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
#     v = askinteger("축소", "\"2\" 또는 \"4\" 또는 \"8\"만 입력", minvalue=2, maxvalue=8)
#     # 중요! 출력 영상 크기 결정
#     outH = inH // v
#     outW = inW // v
#     # 크기 결정되었으니 메모리 할당
#     outImage = []
#     outImage = malloc(outH, outW)
#     # 진짜 컴퓨터 비전 알고리즘이 여기부터 시작
#     for i in range(outH):
#         for k in range(outW):
#             sum = 0
#             for l in range(v):
#                 for m in range(v):
#                     sum += inImage[i * v + l][k * v + m]
#                     outImage[i][k] = sum // (v*v)
#     displayImage()

# 축소 (평균 변환) 알고리즘
def downsizeImage():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    v = askinteger("축소", "\"2\" 또는 \"4\" 또는 \"8\"만 입력", minvalue=2, maxvalue=8)
    # 중요! 출력 영상 크기 결정
    outH = inH // v
    outW = inW // v
    # 크기 결정되었으니 메모리 할당
    outImage = []
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘이 여기부터 시작
    for i in range(inH):
        for k in range(inW):
            outImage[i//v][k//v] += inImage[i][k]
    for i in range(outH):
        for k in range(outW):
            outImage[i][k] //= (v*v)
    displayImage()

# 축소 알고리즘
def downsizeImage2():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    scale = askinteger("축소", "값 (\"2\" 또는 \"4\" 또는 \"8\"만 입력)", minvalue=2, maxvalue=8)
    # 중요! 출력 영상 크기 결정
    # 지금은 동일 영상이니까 크기 같음
    outH = inH // scale
    outW = inW // scale
    # 크기 결정되었으니 메모리 할당
    outImage = []
    outImage = malloc(outH, outW)
    # # 진짜 컴퓨터 비전 알고리즘이 여기부터 시작
    # for i in range(inH):
    #     for k in range(inW):
    #         outImage[i//scale][k//scale] = inImage[i][k]
    # 성능 개선 (forward방식이 아닌 backward 방식으로)
    for i in range(outH):
        for k in range(outW):
            outImage[i][k] = inImage[i*scale][k*scale]
    displayImage()

# 오른쪽 90도 회전 알고리즘
def clock90Image():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정
    outH = inW
    outW = inH
    # 크기 결정되었으니 메모리 할당
    outImage = []
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘이 여기부터 시작
    for i in range(inH):
        l = 127 - i
        for k in range(inW):
            m = k
            outImage[m][l] = inImage[i][k]
    displayImage()

# 회전 알고리즘
def rotateImage():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    angle = askinteger("회전", "각도 입력", minvalue=1, maxvalue=360)
    # 중요! 출력 영상 크기 결정
    # 지금은 동일 영상이니까 크기 같음
    outH = inH
    outW = inW
    # 크기 결정되었으니 메모리 할당
    outImage = []
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘이 여기부터 시작
    # angle(degree)를 라디안으로 바꾸기
    radian = (angle * math.pi) / 180
    for i in range(inH):
        for k in range(inW):
            xs = i
            ys = k
            xd = int(math.cos(radian) * xs - math.sin(radian) * ys)
            yd = int(math.sin(radian) * xs + math.cos(radian) * ys)
            if 0 <= xd < inH and 0<= yd < inW:
                outImage[xd][yd] = inImage[i][k]
    displayImage()


# 회전2 알고리즘 - 중심, 역방향
def rotateImage2():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    angle = askinteger("회전", "각도 입력", minvalue=1, maxvalue=360)
    # 중요! 출력 영상 크기 결정
    # 지금은 동일 영상이니까 크기 같음
    outH = inH
    outW = inW
    # 크기 결정되었으니 메모리 할당
    outImage = []
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘이 여기부터 시작
    # angle(degree)를 라디안으로 바꾸기
    radian = (angle * math.pi) / 180
    cx = inW//2
    cy = inH//2
    for i in range(outH):
        for k in range(outW):
            xs = i
            ys = k
            xd = int(math.cos(radian) * (xs-cx) - math.sin(radian) * (ys-cy)) + cx
            yd = int(math.sin(radian) * (xs-cx) + math.cos(radian) * (ys-cy)) + cy
            if 0 <= xd < inH and 0<= yd < inW:
                outImage[xs][ys] = inImage[xd][yd]
            else:
                outImage[xs][ys] = 255
    displayImage()

# 히스토그램
import matplotlib.pyplot as plt
def histoImage():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    inCountList = [0] * 256
    outCountList = [0] * 256
    for i in range(inH):
        for k in range(inW):
            inCountList[inImage[i][k]] += 1
    for i in range(outH):
        for k in range(outW):
            outCountList[outImage[i][k]] += 1
    plt.plot(inCountList)
    plt.plot(outCountList)
    plt.show()

# 히스토그램 -- matplotlib 없이 구현하기
def histoImage2():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    outCountList = [0] * 256
    normalCountList = [0] * 256
    # 빈도수 계산
    for i in range(outH):
        for k in range(outW):
            outCountList[outImage[i][k]] += 1
    maxVal = max(outCountList)
    minVal = min(outCountList)
    High = 256    # y축에 표시할 최대값 (즉 이 정규화는 최대값이 256일때의 비율로 전체 수치를 조정하는 것)
    # 정규화 = (카운트값 - 최소값) * High / (최대값 - 최소값)
    for i in range(len(outCountList)):
        normalCountList[i] = (outCountList[i] - minVal) * High / (maxVal - minVal)
    # 서브 윈도창 생성 후 출력
    subWindow = Toplevel(window)    # Toplevel(window) = "window라는 Tk 밑에 있는 새로운 Tk이다"라는 뜻
    subWindow.geometry("256x256")
    subCanvas = Canvas(subWindow, width=256, height=256)
    subPaper = PhotoImage(width=256, height=256)
    subCanvas.create_image((256//2, 256//2), image = subPaper, state="normal")

    for i in range(len(normalCountList)):
        for k in range(int(normalCountList[i])):
            data = 0
            subPaper.put("#%02x%02x%02x" % (data, data, data), (i, 255-k))
    subCanvas.pack(expand=1, anchor=CENTER)
    subWindow.mainloop()

# 스트레칭(명암대비) 알고리즘
def stretchImage():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정
    # 지금은 동일 영상이니까 크기 같음
    outH = inH
    outW = inW
    # 크기 결정되었으니 메모리 할당
    outImage = []
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘이 여기부터 시작
    maxVal = minVal = inImage[0][0]
    for i in range(inH):
        for k in range(inW):
            if inImage[i][k] < minVal:
                minVal = inImage[i][k]
            elif inImage[i][k] > maxVal:
                maxVal = inImage[i][k]
    for i in range(inH):
        for k in range(inW):
            outImage[i][k] = int(((inImage[i][k] - minVal) / (maxVal - minVal)) * 255)
    displayImage()

# End-In 탐색 알고리즘
def endinImage():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정
    # 지금은 동일 영상이니까 크기 같음
    outH = inH
    outW = inW
    # 크기 결정되었으니 메모리 할당
    outImage = []
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘이 여기부터 시작
    maxVal = minVal = inImage[0][0]
    for i in range(inH):
        for k in range(inW):
            if inImage[i][k] < minVal:
                minVal = inImage[i][k]
            elif inImage[i][k] > maxVal:
                maxVal = inImage[i][k]
    minAdd = askinteger("최소", "최소에서 추가 값", minvalue=0, maxvalue=255)
    maxAdd = askinteger("최대", "최대에서 감소 값", minvalue=0, maxvalue=255)
    minVal += minAdd
    maxVal -= maxAdd
    for i in range(inH):
        for k in range(inW):
            value = int(((inImage[i][k] - minVal) / (maxVal - minVal)) * 255)
            if value < 0:
                value = 0
            elif value > 255:
                value = 255
            outImage[i][k] = value
    displayImage()

# 히스토그램 평활화 알고리즘
def histoeqImage():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정
    # 지금은 동일 영상이니까 크기 같음
    outH = inH
    outW = inW
    # 크기 결정되었으니 메모리 할당
    outImage = []
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘이 여기부터 시작
    histo = [0] * 256
    sumHisto = [0] * 256
    normalHisto = [0] * 256
    # 히스토그램
    for i in range(inH):
        for k in range(inW):
            histo[inImage[i][k]] += 1
    # 누적 히스토그램
    sValue = 0
    for i in range(len(histo)):
        sValue += histo[i]
        sumHisto[i] = sValue
    # 정규화 누적 히스토그램
    for i in range(len(sumHisto)):
        normalHisto[i] = int(sumHisto[i] / (inW*inH) * 255)
    # 영상 처리
    for i in range (inH):
        for k in range (inW):
            outImage[i][k] = normalHisto[inImage[i][k]]
    displayImage()

# 엠보싱 처리 알고리즘
def embossImage():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정
    # 지금은 동일 영상이니까 크기 같음
    outH = inH
    outW = inW
    # 크기 결정되었으니 메모리 할당
    outImage = []
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘이 여기부터 시작
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
            tmpInImage[i+(MSIZE//2)][k+(MSIZE//2)] = inImage[i][k]
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
            outImage[i][k] = int(value)
    displayImage()

# 블러 처리 알고리즘
def blurImage():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정
    # 지금은 동일 영상이니까 크기 같음
    outH = inH
    outW = inW
    # 크기 결정되었으니 메모리 할당
    outImage = []
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘이 여기부터 시작
    MSIZE = 3
    mask = [[1/9, 1/9, 1/9],
            [1/9, 1/9, 1/9],
            [1/9, 1/9, 1/9]]
    # 임시 입력 영상 메모리 확보
    tmpInImage = malloc(inH+(MSIZE-1), inW+(MSIZE-1), 127)
    tmpOutImage = malloc(outH, outW)
    # 원 입력 --> 임시 입력
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i+(MSIZE//2)][k+(MSIZE//2)] = inImage[i][k]
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
            outImage[i][k] = int(value)
    displayImage()

# 샤프닝 처리 알고리즘
def sharpenImage():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정
    # 지금은 동일 영상이니까 크기 같음
    outH = inH
    outW = inW
    # 크기 결정되었으니 메모리 할당
    outImage = []
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘이 여기부터 시작
    MSIZE = 3
    mask = [[  0, -1,  0],
            [ -1,  5, -1],
            [  0, -1,  0]]
    # 임시 입력 영상 메모리 확보
    tmpInImage = malloc(inH+(MSIZE-1), inW+(MSIZE-1), 127)
    tmpOutImage = malloc(outH, outW)
    # 원 입력 --> 임시 입력
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i+(MSIZE//2)][k+(MSIZE//2)] = inImage[i][k]
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
            outImage[i][k] = int(value)
    displayImage()

# 가우시안 필터링 알고리즘
def gaussImage():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정
    # 지금은 동일 영상이니까 크기 같음
    outH = inH
    outW = inW
    # 크기 결정되었으니 메모리 할당
    outImage = []
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘이 여기부터 시작
    MSIZE = 3
    mask = [[1/16, 1/8, 1/16],
            [ 1/8, 1/4,  1/8],
            [1/16, 1/8, 1/16]]
    # 임시 입력 영상 메모리 확보
    tmpInImage = malloc(inH+(MSIZE-1), inW+(MSIZE-1), 127)
    tmpOutImage = malloc(outH, outW)
    # 원 입력 --> 임시 입력
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i+(MSIZE//2)][k+(MSIZE//2)] = inImage[i][k]
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
            outImage[i][k] = int(value)
    displayImage()

# 고주파 필터 샤프닝 알고리즘
def hpfsharpenImage():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정
    # 지금은 동일 영상이니까 크기 같음
    outH = inH
    outW = inW
    # 크기 결정되었으니 메모리 할당
    outImage = []
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘이 여기부터 시작
    MSIZE = 3
    mask = [[-5,  -5, -5],
            [-5,  40, -5],
            [-5,  -5, -5]]
    # 임시 입력 영상 메모리 확보
    tmpInImage = malloc(inH+(MSIZE-1), inW+(MSIZE-1), 127)
    tmpOutImage = malloc(outH, outW)
    # 원 입력 --> 임시 입력
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i+(MSIZE//2)][k+(MSIZE//2)] = inImage[i][k]
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
            outImage[i][k] = int(value)
    displayImage()

# 저주파 필터 샤프닝 알고리즘: 원 영상 - 고주파
def lpfsharpenImage():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정
    # 지금은 동일 영상이니까 크기 같음
    outH = inH
    outW = inW
    # 크기 결정되었으니 메모리 할당
    outImage = []
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘이 여기부터 시작
    MSIZE = 3
    mask = [[1/9, 1/9, 1/9],
            [1/9, 1/9, 1/9],
            [1/9, 1/9, 1/9]]
    # 임시 입력 영상 메모리 확보
    tmpInImage = malloc(inH+(MSIZE-1), inW+(MSIZE-1), 127)
    tmpOutImage = malloc(outH, outW)
    # 원 입력 --> 임시 입력
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i+(MSIZE//2)][k+(MSIZE//2)] = inImage[i][k]
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
            outImage[i][k] = int(value)
    displayImage()
    ############################################# 안됨...


# 경계선 검출 알고리즘
def edgeImage():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정
    # 지금은 동일 영상이니까 크기 같음
    outH = inH
    outW = inW
    # 크기 결정되었으니 메모리 할당
    outImage = []
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘이 여기부터 시작
    MSIZE = 3
    mask = [[ 0, 0, 0],
            [-1, 1, 0],
            [ 0, 0, 0]]
    # 임시 입력 영상 메모리 확보
    tmpInImage = malloc(inH+(MSIZE-1), inW+(MSIZE-1), 127)
    tmpOutImage = malloc(outH, outW)
    # 원 입력 --> 임시 입력
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i+(MSIZE//2)][k+(MSIZE//2)] = inImage[i][k]
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
            outImage[i][k] = int(value)
    displayImage()

# 모핑 알고리즘
def morphImage():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정
    outH = inH
    outW = inW
    # 추가 영상 선택
    filename2 = askopenfilename(parent=window,
                               filetypes=(("RAW 파일", "*.raw"), ("모든 파일", "*.*")))
    if filename2 == "" or filename2 == None:
        return
    fsize = os.path.getsize(filename2)  # 파일의 크기 (바이트)
    inH2 = inW2 = int(math.sqrt(fsize))  # 핵심 코드
    # 입력 영상 메모리 확보
    inImage2 = []
    inImage2 = malloc(inH2, inW2)
    # 파일에서 메모리로 가져오기
    with open(filename2, "rb") as rFp:  # rb = binary
        for i in range(inH2):
            for k in range(inW2):
                inImage2[i][k] = int(ord(rFp.read(1)))
    # 크기 결정되었으니 메모리 할당
    outImage = []
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘이 여기부터 시작
    w1 = askinteger("원 영상 가중치", "가중치 (%)", minvalue = 0, maxvalue = 100)
    w2 = 1 - (w1/100)
    w1 = 1 - w2
    for i in range(inH):
        for k in range(inW):
            newValue = int(inImage[i][k] * w1 + inImage2[i][k] * w2)
            if newValue > 255:
                newValue = 255
            elif newValue < 0:
                newValue = 0
            outImage[i][k] = newValue
    displayImage()












##########################
##### 전역 변수 선언부 #####
##########################

inImage, outImage = [], []
inH, inW, outH, outW, dispW, dispH = [0] * 6

window, canvas, paper = None, None, None
filename = ""

panYN = False
sx, sy, ex, ey = [0] * 4

VIEW_X, VIEW_Y = 512, 512 # 화면에 보일 크기 (출력용)


#####################
##### 메인 코드부 #####
#####################

window = Tk()
window.geometry("500x500")
window.title("컴퓨터 비전 (딥러닝 기법) Ver 0.03")

status = Label(window, text = "이미지 정보: ", bd = 1, relief = SUNKEN, anchor = W)
status.pack(side=BOTTOM, fill=X)



mainMenu = Menu(window)
window.config(menu=mainMenu)

fileMenu = Menu(mainMenu)
mainMenu.add_cascade(label="파일", menu=fileMenu)
fileMenu.add_command(label="파일 열기", command=openImage)
fileMenu.add_separator()
fileMenu.add_command(label="파일 저장", command=saveImage)

comVisionMenu1 = Menu(mainMenu)
mainMenu.add_cascade(label="화소점 처리", menu=comVisionMenu1)
comVisionMenu1.add_command(label="밝게/어둡게 하기", command=addminusImage)
comVisionMenu1.add_command(label="영상 곱셈", command=multiplyImage)
comVisionMenu1.add_command(label="영상 나눗셈", command=divideImage)
comVisionMenu1.add_command(label="화소값 반전", command=reverseImage)
comVisionMenu1.add_command(label="Posterization", command=posterizeImage)
comVisionMenu1.add_command(label="파라볼라", command=paraImage)
comVisionMenu1.add_separator()
comVisionMenu1.add_command(label="모핑", command=morphImage)

comVisionMenu2 = Menu(mainMenu)
mainMenu.add_cascade(label="화소 (통계)", menu=comVisionMenu2)
comVisionMenu2.add_command(label="이진화 (= 흑백)", command=bwImage)
comVisionMenu2.add_command(label="입력/출력 영상 평균값", command=avgImage)
comVisionMenu2.add_command(label="축소 (평균 변환)", command=downsizeImage)
comVisionMenu2.add_command(label="확대 (양선형 보간)", command=upsizeImage2)
comVisionMenu2.add_separator()
comVisionMenu2.add_command(label="히스토그램", command=histoImage)
comVisionMenu2.add_command(label="히스토그램 (시각화 연습)", command=histoImage2)
comVisionMenu2.add_command(label="명암대비", command=stretchImage)
comVisionMenu2.add_command(label="End-In 탐색", command=endinImage)
comVisionMenu2.add_command(label="히스토그램 평활화", command=histoeqImage)

comVisionMenu3 = Menu(mainMenu)
mainMenu.add_cascade(label="기하학 처리", menu=comVisionMenu3)
comVisionMenu3.add_command(label="상하 반전", command=updownImage)
comVisionMenu3.add_command(label="이동 (상하/좌우)", command=moveImage)
comVisionMenu3.add_command(label="확대", command=upsizeImage)
comVisionMenu3.add_command(label="축소", command=downsizeImage2)
comVisionMenu3.add_command(label="오른쪽 90도 회전", command=clock90Image)
comVisionMenu3.add_command(label="회전", command=rotateImage)
comVisionMenu3.add_command(label="회전2 (중심, 역방향)", command=rotateImage2) #

comVisionMenu4 = Menu(mainMenu)
mainMenu.add_cascade(label="화소 영역 처리", menu=comVisionMenu4)
comVisionMenu4.add_command(label="엠보싱 처리", command=embossImage)
comVisionMenu4.add_command(label="블러 처리", command=blurImage)
comVisionMenu4.add_command(label="샤프닝 처리", command=sharpenImage)
comVisionMenu4.add_command(label="가우시안 필터링", command=gaussImage)
comVisionMenu4.add_command(label="고주파 필터 샤프닝", command=hpfsharpenImage)
comVisionMenu4.add_command(label="저주파 필터 샤프닝", command=lpfsharpenImage) #
comVisionMenu4.add_command(label="경계선 검출", command=edgeImage)



window.mainloop()


