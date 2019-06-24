## 4일차 퀴즈 1: 10크기의 영상 데이터를 랜덤하게 준비한 후, 영상에 밝기를 더한다 (10을 더하기). 출력은 원영상, 밝아진 영상.

import random
SIZE = 10

aa = []
for _ in range(SIZE):
    aa.append(0)

for i in range(SIZE):
    num = random.randint(0,255)
    aa[i] = num
print("원 영상 --> ", aa)

for i in range(SIZE):
    aa[i] += 10
    if aa[i] > 255:    # 영상 밝기는 0~255이므로 255를 넘어가면 안된다.
        aa[i] = 255
print("결과 영상 --> ", aa)

