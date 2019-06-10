# 중첩 for문

## 구구단 출력

```python
i, k = 0, 0

for i in range (2, 10, 1):
    print("## %d단 ##" % (i))
    for k in range (1, 10, 1):
        print(i, "*", k, "=", i*k)
```



## 10 x 10 크기의 숫자를 예쁘게 출력해라

```python
count = 0
for _ in range (10):
    for _ in range (10):
        print ("%2d " % (count), end = '')
        count += 1
    print()
```



## 10 x 10 크기의 칸에 숫자를 랜덤으로 넣기

```python
import random
import random as rd    # 이름 줄일 때
from random import randrange, randint    # 아예 사용할 것 지정 (ramdom.randrange 가 아니라 randrange로 바로 쓸 수 있음)
from random import *    # random 안의 모든 것 import

for _ in range (10):
    for _ in range (10):
        num = randrange(0, 100) # randint(0, 99)
        print ("%2d " % (num), end = '')
    print()
```



# 리스트

## 4개의 랜덤한 숫자를 리스트에 저장한 후, 합계를 계산

### Ver.1

```python
import random

aa = [0, 0, 0, 0]     # 4칸의 리스트 준비

for i in range (4):  # range(0, 4, 1)
    num = random.randint(0, 99)
    aa[i] = num

print(aa)
```

### Ver.2

```python
import random

aa = []     # 비어있는 리스트 준비

for i in range (4):  # range(0, 4, 1)
    num = random.randint(0, 99)
    aa.append(num)    # append: 리스트에 칸 추가

print(aa)
```

### Ver.3

```python
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
```



# Quiz 1

10크기의 영상 데이터를 랜덤하게 준비한 후, 영상에 밝기를 더한다 (10을 더하기).

출력은 원영상, 밝아진 영상.

```python
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
```



# 리스트 조작 함수

## 특정 값의 모든 위치를 출력하는 프로그램

### Ver.1

```python
import random
myList = [random.randint(1,5) for _ in range(10)]
print(myList)

NUMBER = 5

index = 0
while True:
    try:
        index = myList.index(NUMBER, index)
        print(index)
        index += 1
    except:
        break
```

### Ver.2

```python
import random
myList = [random.randint(1,5) for _ in range(10)]
print(myList)

NUMBER = 5

index = 0

for i in range (myList.count(NUMBER)):
    index = myList.index(NUMBER, index)
    print(index)
    index += 1
```



# 자료 구조

* Stack
  * 바닥이 막힌 병에 차례로 넣는다. 그럼 넣은 순서의 반대로 뺄 수 있다. 이게 stack 구조.
  * FILO (First In Last Out)
* Que
  * 줄 서 있는 구조. 입구와 출구가 다르다.
  * FIFO (First In First Out)



# sorted와 sort의 차이

* sorted(myList) 하면 보여주는 방식만 정렬한거고 리스트 자체는 안바뀐다
* myList.sort()하면 리스트 자체가 정렬되어 바뀐다



# 리스트 복사 시 주의 사항

* 그냥 "="으로 복사하면 shallow copy되어 한 개를 변형하면 두개가 다 변형된다 (교재 p.209 참고)
* 그러므로 copy를 써야 한다.
  * newList = myList.copy()
* 혹은 [:]을 쓴다.
  * newList = myList[:]



# 2차원 리스트

리스트 안에 리스트가 들어간 것

```python
##### 3x4 크기의 리스트 조작하기

# 1. 2차원 빈 리스트 생성
# image = [[0, 0, 0, 0],
#         [0, 0, 0, 0],
#         [0, 0, 0, 0]]
ROW, COL = 10, 10
image = []
temp = []
for i in range(ROW):
    temp=[]
    for k in range(COL):
        temp.append(0)
    image.append(temp)

# 2. 대입 --> 파일에서 로딩...
import random
for i in range (ROW):
    for k in range (COL):
        image[i][k] = random.randint(0,255)

# 3. 데이터 처리/변환/분석 ... --> 영상 밝게 하기 (+100)
for i in range (ROW):
    for k in range (COL):
        image[i][k] += 100

# 4. 데이터 출력
for i in range (ROW):
    for k in range (COL):
        print("%3d " % (image[i][k]), end="")
    print()
```



# 튜플

읽기 전용 리스트

* 수정만 안되고 리스트랑 똑같다



# 딕셔너리

* {키:값, 키:값, … , 키:값}
* 중요한 특징
  * 키는 중복이 되면 안된다.
  * 순서가 없다.

* 키에 값을 넣을 때, 키가 기존에 없는 키면 추가되고, 있는 키면 값이 변경된다 (왜냐하면 키는 중복될 수 없으니까)

```python
## 딕셔너리 활용 ##

import operator

ttL = [("토마스", 5), ("헨리", 8), ("에드워드", 9), ("토마스", 12), ("에드워드", 1)]    # train tuple List

tD = {}    # train Dictionary
tL = []    # train List
tR, cR = 1, 1    # total Rank, current Rank

for tmpTup in ttL:
    tName = tmpTup[0]
    tWeight = tmpTup[1]
    if tName in tD:
        tD[tName] += tWeight
    else:
        tD[tName] = tWeight
print(list(tD.items()))
tL = sorted(tD.items(), key=operator.itemgetter(1), reverse = True)  # 정렬하는데, key를 index 1번째 항목으로 정렬
print(tL)

print("------------------------")
print("기차\t총 수송량\t순위")
print("------------------------")
print(tL[0][0], "\t", tL[0][1], "\t", cR)
for i in range(1, len(tL)):
    tR += 1
    if tL[i][1] == tL[i-1][1]:    # 앞 기차와 수송량이 같다면
        pass
    else:
        cR = tR
    print(tL[i][0], "\t", tL[i][1], "\t", cR)
```



# 프로그래밍 패러다임

* 절차적 프로그래밍 → 구조적 프로그래밍 → 객체 지향 프로그래밍
* 절차적 프로그래밍의 한계
  * 윗줄부터 차례차례 실행
  * 같은 코드도 여러 번 써야 함
  * 그래서 유지보수가 힘들다 → 여러 번 쓴 코드를 수정하려면 여러 번 수정해야 함
  * 그래서 함수개념이 도입된 구조적 프로그래밍이 도입됨
* 구조적 프로그래밍
  * C언어 등
  * 함수 사용
    * 유지보수 시 함수만 수정하면 되므로 편리
    * 모듈: 함수의 묶음



# 함수

```python
## 두 수를 받아서 더한 값을 반환하는 함수
def plus(v1, v2):
    result = 0
    result = v1 + v2
    return result


## 메인 코드 부 ##
hap = plus(100,200)
print(hap)
hap = plus(200,300)
print(hap)
hap = plus(300,400)
print(hap)
```

* 함수는 반환값이 있을 수도 있고 없을 수도 있다
  * 하지만 대부분의 함수는 반환값이 있다



# 전역변수와 지역변수

```python
def func1():
    global a    # 아래 나올 a는 전역변수라고 지정하는 것
    a = 10     # 원래 여기서 a는 지역변수 -- 자기 지역에서만 살아있는 함수 (대개는 지역이 함수)
    print("func1() --> ", a)

def func2():
    global a
    print("func2() --> ", a)    # func2에서는 a가 없으므로 밖에서 찾는다



## 변수 선언부 ##
a = 1234     # 여기서 a는 전역변수



## 메인 코드부 ##
func1()
print(a)    # a가 10으로 변경되어 있기를 기대함
func2()
```

* 지역변수는 자기 지역에서만 살아있는 함수 (대개는 지역이 함수)
* "global (변수이름)"을 통해 전역변수로 선언할 수 있다
  * 보통은 전역변수랑 지역변수의 이름을 구분하기 위해 전역변수 이름은 맨 앞에 소문자 g를 붙인다 (예: gABC)



# 반환값과 매개변수

```python
## 두 수를 받아서 더한 값을 반환하는 함수
def calc(v1, v2, v3 = 0):
    result1 = v1 + v2 + v3
    result2 = v1 - v2 - v3
    return result1, result2    # 파이썬에서는 반환값이 여러개일 수 있다
def calc2(*para):
    res = 0
    for num in para:
        res += num
    return res


## 메인 코드 부 ##
hap1, hap2 = calc(100,200,300)
hap = calc2(12,3,3,4,5,6,7)
print(hap)
```



# 모듈

모듈: 함수의 모음



# 내부 함수

```python
def outFunc(v1, v2):
    def inFunc(n1, n2):
        return n1+n2
    return inFunc(v1, v2)
print(outFunc(100, 200))
```



# Lambda

```python
def hap(v1, v2):
    res = v1 + v2
    return res
hap2 = lambda v1, v2: v1+v2    # 함수 hap과 hap2는 똑같다
print(hap(100,200))
print(hap2(100,200))
```



# map()

```python
myList = [1,2,3,4,5]

# def add10(num):
#     return num+10
add10 = lambda num: num+10

# for i in range(len(myList)):
#     myList[i] = add10(myList[i])
myList = list(map(add10, myList))

print(myList)

# 혹은

myList = [1,2,3,4,5]

myList = list(map(lambda num: num+10, myList))

print(myList)
```

