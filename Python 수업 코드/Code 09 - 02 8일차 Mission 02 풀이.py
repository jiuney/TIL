from tkinter import *
from tkinter.simpledialog import *
from tkinter.filedialog import *
import math
import os
import os.path
import struct
import pymysql
import datetime
import tempfile



#####################
##### 전역 변수부 #####
#####################

IP_ADDR = "192.168.56.109"
USER_NAME = "root"
USER_PW = "1234"
DB_NAME = "BigData_DB"
CHAR_SET = "utf8"

fnameList = []
inImage = []


#################
##### 함수부 #####
#################

def malloc(h, w, initValue=0):
    retMemory = []
    for _ in range (h):
        tmpList = []
        for _ in range (w):
            tmpList.append(initValue)
        retMemory.append(tmpList)
    return retMemory

def selectFile():
    filename = askopenfilename(parent=window,
                               filetypes=(("RAW 파일", "*.raw"), ("모든 파일", "*.*")))
    if filename == "" or filename == None:
        return
    edt1.insert(0, str(filename))

def selectFolder():
    folder = askdirectory(parent=window)
    for dirName, subDirList, fnames in os.walk(folder):
        for fname in fnames:
            fullName = dirName + '/' + fname
            fnameList.append(fullName)
    edt1.insert(0, str(folder))

def selectFolder2():
    global rawFileList
    foldername = askdirectory(parent=window)
    if foldername == "" or foldername == None:
        return
    edt1.insert(0, str(foldername))
    # 파일 목록 뽑기
    rawFileList = []
    for dirName, subDirList, fnames in os.walk(foldername):
        for fname in fnames:
            filename, extname = os.path.basename(fname).split(".")
            if extname.upper().strip() == "RAW":     # strip(): 문자열 앞뒤 공백 잘라주는 함수
                rawFileList.append(os.path.join(dirName,fname))

def uploadData():
    con = pymysql.connect(host=IP_ADDR, user=USER_NAME, password=USER_PW, db=DB_NAME, charset=CHAR_SET)
    cur = con.cursor()

    fullname = edt1.get()

    fname = os.path.basename(fullname)
    fsize = os.path.getsize(fullname)
    height = width = int(math.sqrt(fsize))
    now = datetime.datetime.now()
    upDate = now.strftime("%Y-%m-%d")
    upUser = USER_NAME

    inImage = malloc(height, width)
    with open(fullname, "rb") as rfp:    # rb = read binary
        for i in range (height):
            for k in range (width):
                inImage[i][k] = int(ord(rfp.read(1)))
    with open(fullname, "rb") as rfp:  # rb = read binary
        binData = rfp.read()

    # 영상 평균값
    avg = 0
    sum = 0
    for i in range(height):
        for k in range(width):
            sum += inImage[i][k]
    avg = sum / (height * width)

    # 영상 최소값
    min = 255
    for i in range(height):
        for k in range(width):
            if min > inImage[i][k]:
                min = inImage[i][k]

    # 영상 최대값
    max = 0
    for i in range(height):
        for k in range(width):
            if max < inImage[i][k]:
                max = inImage[i][k]

    sql = "INSERT INTO rawImage_TBL(raw_id, raw_width, raw_height, raw_fname, raw_avg, raw_min, raw_max, raw_update, raw_uploader, raw_data)"
    sql += " VALUES(NULL, " + str(width) + ", " + str(height) + ",'" + fname + "', " + str(avg) + ", " + str(min) + ", " + str(max) + ", '" + upDate + "', '" + upUser + "', %s)"

    tupleData = (binData)
    cur.execute(sql, tupleData)

    con.commit()
    cur.close()
    con.close()

def uploadData2():
    con = pymysql.connect(host=IP_ADDR, user=USER_NAME, password=USER_PW, db=DB_NAME, charset=CHAR_SET)
    cur = con.cursor()

    for i in range(len(fnameList)):
        fullname = fnameList[i]

        fname = os.path.basename(fullname)
        fsize = os.path.getsize(fullname)
        height = width = int(math.sqrt(fsize))
        now = datetime.datetime.now()
        upDate = now.strftime("%Y-%m-%d")
        upUser = USER_NAME

        inImage = malloc(height, width)
        with open(fullname, "rb") as rfp:  # rb = read binary
            for i in range(height):
                for k in range(width):
                    inImage[i][k] = int(ord(rfp.read(1)))
        with open(fullname, "rb") as rfp:    # rb = read binary
            binData = rfp.read()

        # 영상 평균값
        avg = 0
        sum = 0
        for i in range(height):
            for k in range(width):
                sum += inImage[i][k]
        avg = sum / (height * width)

        # 영상 최소값
        min = 255
        for i in range(height):
            for k in range(width):
                if min > inImage[i][k]:
                    min = inImage[i][k]

        # 영상 최대값
        max = 0
        for i in range(height):
            for k in range(width):
                if max < inImage[i][k]:
                    max = inImage[i][k]

        sql = "INSERT INTO rawImage_TBL(raw_id, raw_width, raw_height, raw_fname, raw_avg, raw_min, raw_max, raw_update, raw_uploader, raw_data)"
        sql += " VALUES(NULL, " + str(width) + ", " + str(height) + ",'" + fname + "', " + str(avg) + ", " + str(min) + ", " + str(max) + ", '" + upDate + "', '" + upUser + "', %s)"

        tupleData = (binData)
        cur.execute(sql, tupleData)

        con.commit()

    cur.close()
    con.close()

def findStat(fname):
    # 파일 열고, 읽기.
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
    sum = 0
    for i in range(inH):
        for k in range(inW):
            sum += inImage[i][k]
    avg = sum / (inH*inW)
    maxVal = minVal = inImage[0][0]
    for i in range(inH):
        for k in range(inW):
            if inImage[i][k] < minVal:
                minVal = inImage[i][k]
            elif inImage[i][k] > maxVal:
                maxVal = inImage[i][k]
    return avg, maxVal, minVal

def uploadData3():
    global rawFileList
    con = pymysql.connect(host=IP_ADDR, user=USER_NAME, password=USER_PW, db=DB_NAME, charset=CHAR_SET)
    cur = con.cursor()

    try:
        sql = "CREATE TABLE rawImage2_TBL (raw_id INT AUTO_INCREMENT PRIMARY KEY, raw_fname VARCHAR(30), raw_extname CHAR(5), raw_height SMALLINT, raw_width SMALLINT, raw_avg TINYINT UNSIGNED, raw_max TINYINT UNSIGNED, raw_min TINYINT UNSIGNED, raw_data LONGBLOB);"
        cur.execute(sql)
    except:
        pass

    for fullname in rawFileList:
        with open(fullname, "rb") as rfp:    # rb = read binary
            binData = rfp.read()

        fname, extname = os.path.basename(fullname).split(".")
        fsize = os.path.getsize(fullname)
        height = width = int(math.sqrt(fsize))

        avgVal, maxVal, minVal = findStat(fullname)    # 평균, 최대, 최소


        sql = "INSERT INTO rawImage2_TBL (raw_id, raw_fname, raw_extname, raw_height, raw_width, raw_avg, raw_max, raw_min, raw_data)"
        sql += " VALUES(NULL, '" + fname + "', '" + extname + "', " + str(height) + ", " + str(width) + ", " + str(avgVal) + ", " + str(maxVal) + ", " + str(minVal) + ", %s)"

        tupleData = (binData,)
        cur.execute(sql, tupleData)
        con.commit()
        print("업로드 OK --> " + fullname)
    cur.close()
    con.close()
    print("끝!!")

def downloadData():
    con = pymysql.connect(host=IP_ADDR, user=USER_NAME, password=USER_PW, db=DB_NAME, charset=CHAR_SET)
    cur = con.cursor()

    sql = "SELECT raw_fname, raw_data FROM rawImage_TBL WHERE raw_id = 1"
    cur.execute(sql)
    fname, binData = cur.fetchone()

    # 모든 windows 컴퓨터에 있는 temp 폴더에 저장하기
    fullPath = tempfile.gettempdir() + "/" + fname
    with open(fullPath, "wb") as wfp:    # wb = write binary
        wfp.write(binData)
    print(fullPath)

    con.commit()
    cur.close()
    con.close()












#####################
##### 메인 코드부 #####
#####################

window = Tk()
window.geometry("500x200")
window.title("Raw --> DB Ver 0.02")

edt1 = Entry(window, width=50)
edt1.pack()
btnFile = Button(window, text="파일 선택", command=selectFile)
btnFile.pack()
btnFolder = Button(window, text="폴더 선택", command=selectFolder)
btnFolder.pack()
btnFolder2 = Button(window, text="폴더 선택2", command=selectFolder2)
btnFolder2.pack()
btnUpload = Button(window, text="업로드 파일", command=uploadData)
btnUpload.pack()
btnUpload2 = Button(window, text="업로드 폴더", command=uploadData2)
btnUpload2.pack()
btnUpload3 = Button(window, text="업로드 폴더2", command=uploadData3)
btnUpload3.pack()
btnDownload = Button(window, text="다운로드", command=downloadData)
btnDownload.pack()

window.mainloop()
