## 4개의 랜덤한 숫자를 리스트에 저장한 후, 합계를 계산하자. ##
## 빈 메모리를 확보한 후에 작업하기. ##

import random
SIZE = 4

# 1. 메모리 확보 개념
aa = []     # 비어있는 리스트 준비
for i in range(SIZE):
    aa.append(0)

# 2. 메모리에 필요한 값 대입 --> 파일 읽기
for i in range (SIZE):
    num = random.randint(0, 99)
    aa[i] = num

# 3. 메모리 처리/조작/연산 --> 알고리즘(컴퓨터 비전, 영상처리)
sum = 0
for i in range(SIZE):
    sum += aa[i]
avg = sum / SIZE

# 4. 출력
print("원 리스트 --> ", aa)
print("리스트 평균값 --> ", avg)

