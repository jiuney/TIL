########## p.283 문자, 숫자 정렬 → 선택 정렬, 버블 정렬, 퀵 정렬 ##########

##### 선택 정렬 #####

import random

## 함수 선언 부분 ##

def getNumber(strData):
    numStr=""
    for ch in strData:
        if ch.isdigit():
            numStr += ch
    return int(numStr)

## 변수 선언 부분 ##

data = []
i, k = 0, 0

## 메인 코드 부분 ##

for i in range (0, 10):
    tmp = hex(random.randrange(0, 100000))
    tmp = tmp[2:]
    data.append(tmp)
print("정렬 전 데이터: ", end = "")
[print(num, end = " ") for num in data]

for i in range (0, len(data)-1):
    for k in range (i+1, len(data)):
        if getNumber(data[i]) > getNumber(data[k]):
            tmp = data[i]
            data[i] = data[k]
            data[k] = tmp
print("\n정렬 후 데이터: ", end = "")
[print(num, end = " ") for num in data]

# 근데 랜덤으로 생성된 문자열들 중 하나에라도 숫자는 없고 문자만 있을 경우 에러가 난다.