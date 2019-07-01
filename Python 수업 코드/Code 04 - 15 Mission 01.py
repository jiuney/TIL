########## p.219 16진수 정렬 → 선택 정렬, 버블 정렬, 퀵 정렬 ##########

##### 선택 정렬 #####

import random

## 변수 선언부 ##

mL = []
i, k = 0, 0

## 메인 코드부 ##

for i in range (0, 10):
    tmp = hex(random.randrange(0, 100000))
    mL.append(tmp)
print("정렬 전 데이터: ", end="")
[print(num, end=" ") for num in mL]

for i in range (0, len(mL)-1):
    for k in range (i+1, len(mL)):
        if int(mL[i], 16) > int(mL[k], 16):
            tmp = mL[i]
            mL[i] = mL[k]
            mL[k] = tmp
print("\n정렬 후 데이터: ", end="")
[print(num, end=" ") for num in mL]



