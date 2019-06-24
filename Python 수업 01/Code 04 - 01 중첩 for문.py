## 구구단 출력 ##

# i, k = 0, 0
#
# for i in range (2, 10, 1):
#     print("## %d단 ##" % (i))
#     for k in range (1, 10, 1):
#         print(i, "*", k, "=", i*k)



## 10 x 10 크기의 숫자를 예쁘게 출력해라 ##

# count = 0
# for _ in range (10):
#     for _ in range (10):
#         print ("%2d " % (count), end = '')
#         count += 1
#     print()



## 10 x 10 크기의 칸에 숫자를 랜덤으로 넣기 ##

import random
import random as rd    # 이름 줄일 때
from random import randrange, randint    # 아예 사용할 것 지정 (ramdom.randrange 가 아니라 randrange로 바로 쓸 수 있음)
from random import *    # random 안의 모든 것 import

for _ in range (10):
    for _ in range (10):
        num = randrange(0, 100) # randint(0, 99)
        print ("%2d " % (num), end = '')
    print()

