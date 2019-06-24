import csv
from tkinter.filedialog import *

filename = askopenfilename(parent=None, filetypes=(("CSV 파일", "*.csv"), ("모든 파일", "*.*")))

csvList = []
with open(filename) as rfp:
    reader = csv.reader(rfp)
    headerList = next(reader)
    sum = 0
    count = 0
    for cList in reader:
        csvList.append(cList)
    print(csvList)



## 가격을 10% 인상시키기.
#1. Cost 열의 위치를 찾아내기.
headerList = [ data.upper().strip() for data in headerList ]    # 헤더의 글자들을 대문자로 통일하고 앞뒤 공백 제거
pos = headerList.index("COST")
for i in range(len(csvList)):
    rowList = csvList[i]
    cost = rowList[pos]
    cost = float(cost[1:])     # 문자열 맨 앞은 "$"이므로 잘라버리고 두번째 ([1]) 부터 값을 갖는다
    # 10% 인상
    cost *= 1.1
    costStr = "${0:.2f}".format(cost)
    csvList[i][pos] = costStr
print(csvList)



## 결과를 저장하기
saveFp = asksaveasfile(parent=None, mode='wt', defaultextension="*.csv", filetypes=(("CSV 파일", "*.csv"), ("모든 파일", "*.*")))
with open(saveFp.name, mode="w", newline="") as wFp:    # newline=""을 넣어야 쓸 때 한줄씩 건너뛰는걸 막을 수 있다.
    writer = csv.writer(wFp)
    writer.writerow(headerList)
    for row in csvList:
        writer.writerow(row)

