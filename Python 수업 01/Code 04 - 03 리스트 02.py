## 4개의 랜덤한 숫자를 리스트에 저장한 후, 합계를 계산하자. ##

import random

aa = []     # 비어있는 리스트 준비

for i in range (4):  # range(0, 4, 1)
    num = random.randint(0, 99)
    aa.append(num)    # append: 리스트에 칸 추가

print(aa)

