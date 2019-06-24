from tkinter import *
from tkinter.simpledialog import *
from tkinter.filedialog import *
import math
import os
import os.path
import struct



#######################
##### 함수 선언부 #####
#######################

# 메모리를 할당해서 리스트(참조)를 반환하는 함수
def malloc(h, w):    # malloc = memory allocate
    retMemory = []
    for _ in range (h):
        tmpList = []
        for _ in range (w):
            tmpList.append(0)
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

def displayImage():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    if canvas!= None:    # 예전에 실행한 적이 있다면
        canvas.destroy()
    # 화면 크기를 조절
    window.geometry(str(outH)+"x"+str(outW))    # 벽
    canvas = Canvas(window, height = outH, width = outW)    # 보드
    paper = PhotoImage(height = outH, width = outW)    # 빈 종이
    canvas.create_image((outH//2, outW//2), image = paper, state = "normal")
    # # 출력 영상을 화면에 한 점씩 찍기
    # for i in range(outH):
    #     for k in range(outW):
    #         r = g = b = outImage[i][k]   # r = g = b 인 이유는 지금 grayscale이므로
    #         paper.put("#%02x%02x%02x" % (r, g, b), (k, i))    # (i,k)가 아니고 (k,i)인 이유는 데이터 저장 상태가 기울어져 있으므로 제대로 표시되려면 위치를 바꿔줘야 하므로 이렇게 함.
    # 성능 개선
    rgbStr = ""    # 전체 픽셀의 문자열을 저장
    for i in range(outH):
        tmpStr = ""
        for k in range(outW):
            r = g = b = outImage[i][k]
            tmpStr += " #%02x%02x%02x" % (r, g, b)    # 문자열에서 한 칸을 꼭 떼 줘야 나중에 자를 수 있다
        rgbStr += "{" + tmpStr + "} "     # 문자열에서 중괄호 끝에 한 칸을 꼭 떼 줘야 나중에 자를 수 있다
    paper.put(rgbStr)
    # 마우스 이벤트
    canvas.bind("<Button-1>", mouseClick)
    canvas.bind("<ButtonRelease-1>", mouseDrop)
    canvas.pack(expand=1, anchor=CENTER)



####################################################
##### 컴퓨터 비전 (영상 처리) 알고리즘 함수 모음 #####
####################################################

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



# 확대 알고리즘
def upsizeImage():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    v = askinteger("확대", "\"2\" 또는 \"4\"만 입력", minvalue=2, maxvalue=4)
    # 중요! 출력 영상 크기 결정
    outH = inH * v
    outW = inW * v
    # 크기 결정되었으니 메모리 할당
    outImage = []
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘이 여기부터 시작
    for i in range(inH):
        for k in range(inW):
            for l in range(v):
                for m in range(v):
                    outImage[i * v + l][k * v + m] = inImage[i][k]
    displayImage()

# 축소 알고리즘
def downsizeImage():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    v = askinteger("확대", "\"2\" 또는 \"4\" 또는 \"8\"만 입력", minvalue=2, maxvalue=8)
    # 중요! 출력 영상 크기 결정
    outH = inH // v
    outW = inW // v
    # 크기 결정되었으니 메모리 할당
    outImage = []
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘이 여기부터 시작
    for i in range(outH):
        for k in range(outW):
            sum = 0
            for l in range(v):
                for m in range(v):
                    sum += inImage[i * v + l][k * v + m]
                    outImage[i][k] = sum // (v*v)
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
    pass     # 모르겠어요...






###########################
##### 전역 변수 선언부 #####
###########################

inImage, outImage = [], []
inH, inW, outH, outW = [0] * 4

window, canvas, paper = None, None, None
filename = ""

panYN = False
sx, sy, ex, ey = [0] * 4



#######################
##### 메인 코드부 #####
#######################

window = Tk()
window.geometry("500x500")
window.title("컴퓨터 비전 (딥러닝 기법) Ver 0.02")



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

comVisionMenu2 = Menu(mainMenu)
mainMenu.add_cascade(label="화소 (통계)", menu=comVisionMenu2)
comVisionMenu2.add_command(label="이진화 (= 흑백)", command=bwImage)
comVisionMenu2.add_command(label="입력/출력 영상 평균값", command=avgImage)

comVisionMenu3 = Menu(mainMenu)
mainMenu.add_cascade(label="기하학 처리", menu=comVisionMenu3)
comVisionMenu3.add_command(label="상하 반전", command=updownImage)
comVisionMenu3.add_command(label="이동 (상하/좌우)", command=moveImage)
comVisionMenu3.add_command(label="확대", command=upsizeImage)
comVisionMenu3.add_command(label="축소", command=downsizeImage)
comVisionMenu3.add_command(label="오른쪽 90도 회전", command=clock90Image)
comVisionMenu3.add_command(label="회전", command=rotateImage)

window.mainloop()


