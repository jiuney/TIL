# Database의 기본

* Data: 단편적인 자료
* Database (DB): data의 저장소
* Table
  * 자료를 저장하는 방식
  * 행 = row = record
    * 데이터는 가로로 저장된다
    * 행의 개수가 데이터의 개수
  * 열 = column = field
    * 열에는 이름이 있다 → field name (column name)
    * 각 열에는 입력될 데이터의 형식이 결정되어 있다 (문자, 숫자, 날짜 등)
    * Primary Key (PK, 기본키)
      * 기본키의 필수 조건 2개
        * 중복되어서는 안된다
        * 반드시 있어야 한다
          * Not Null
      * 기본키의 예
        * 인터넷 사이트 ID
        * 주민등록번호
      * 필수조건을 만족한다고 모두 기본키가 되는것은 아니다
      * 기본키는반드시 테이블 당 한 개
        * 기본키가 될 수 있는 조건을 만족한 열들을 후보키라고도 한다
    * Unique Key
      * 중복만 안되는 key
* Database Management System (DBMS)
  * 데이터베이스를 관리하는 소프트웨어
  * MySQL, MariaDB, SQL Server, …
* Database 관리
  * select문
    * 데이터 선택 (가져오기)
  * SQL (Structured Query Language)
    * DBMS와 소통하는 언어



# Database 관리 실습 (with HeidiSQL)

* 예약어는 대문자, 사용자 지정 언어는 소문자로 써주면 알아보기 쉽다
* 쿼리문의 마지막에는 ";"을 써주는게 약속
* 예약어는 열이름으로 안쓰는게 좋다
* VARCHAR는 variable character
  * character는 고정형 변수로, 크기를 잡아놓으면 그보다 작은 데이터가 들어와도 고정된 크기를 다 사용한다
  * varchar는 가변형으로, 잡아놓은 크기보다 작은 데이터가 들어오면 그만큼만 사용한다
  * 대신 varchar 보다 char가 처리속도가 빠르다
* commit을 해줘야 작업한게 저장된다
  * 취소는 rollback인데 잘 안쓴다
* "*(별표)"는 "전체"를 의미
* 테이블 삭제: DROP TABLE …
* 테이블 변경: ALTER TABLE ...



## 3일차 퀴즈 1~2

Q1. Windows Server의 MariaDB 또는 MySQL에 p423 구현하기

Q2. SQL server에 p423 구현하기

A. 가상머신을 켠 다음에 heidiSQL에서 연결한 후에 다음 쿼리 사용.

```sql
CREATE DATABASE myDBDay3Q1;

USE myDBDay3Q1;

CREATE TABLE userTable (userID CHAR(10), userName CHAR(15), userEmail VARCHAR(50), birthYear SMALLINT );

INSERT INTO userTable VALUES ('john', 'John Bann', 'john@naver.com', 1990)
INSERT INTO userTable VALUES ('kim', 'Kim Chi', 'kim@naver.com', 1992)
INSERT INTO userTable VALUES ('lee', 'Lee Pal', 'lee@naver.com', 1988)
INSERT INTO userTable VALUES ('park', 'Park Su', 'park@naver.com', 1980)

COMMIT;

SELECT * FROM userTable;
```



# Python에서 Database 관리 1

## SQLite 데이터 입력

```python
import sqlite3

conn = sqlite3.connect("samsongDB") # 1. DB 연결
cur = conn.cursor() # 2. 커서 생성 (트럭, 연결로프)
sql = "CREATE TABLE IF NOT EXISTS userTable(userId INT, userName CHAR(5))"
cur.execute(sql)

sql = "INSERT INTO userTable VALUES(1, '홍길동')";
cur.execute(sql)
sql = "INSERT INTO userTable VALUES(2, '이순신')";
cur.execute(sql)

cur.close()
conn.commit()
conn.close() # 6. DB 닫기 (=연결 해제)
print ("OK~")
```

## SQLite 데이터 조회

```python
import sqlite3

conn = sqlite3.connect("samsongDB") # 1. DB 연결
cur = conn.cursor() # 2. 커서 생성 (트럭, 연결로프)
sql = "SELECT * FROM userTable"
cur.execute(sql)

rows = cur.fetchall()

print(rows)

cur.close()
conn.close() # 6. DB 닫기 (=연결 해제)
print ("OK~")
```



# Python 실습

## 계산기 만들기

* 프로그래밍 언어에서는 항상 left value에 right value가 들어간다

* 다음과 같은 코드가 있을 때

  ```python
  a=100
  b=200
  ```

  * a는 변수
    * 담는 그릇
  * 100은 값
    * 내용물
  * 왼쪽에는 항상 변수만 온다
    * 오른쪽에는 내 맘대로

* 다음과 같은 코드가 있을 때

  ```python
  a=100
  b=200
  a=b
  ```

  * a에는 결국 200이 담긴다 -> update된다

* 다음과 같은 코드가 있을 때

  ```python
  a=100
  b=200
  a=b
  b = a + 200
  ```

  * b에는 결국 400이 담긴다
    * =(등호) 는 가장 마지막에 처리된다

* 변수는 항상 4가지 중에 한가지 타입을 갖는다

  * 정수 (Integer)
  * 실수 (Float)
  * 문자열(String)
  * 불 (Bool)

* 다른 프로그래밍 언어들은 변수의 타입을 지정하면 그 타입의 값만 넣어야 하는데, python에서는 유연하게 변경할 수 있다
  
  * 예: a에 100을 넣었다가 "ㅋㅋㅋ"를 넣을 수 있다

```python
a = int(input("숫자 1-->"))
b = int(input("숫자 2-->"))

result = a + b
print(a, "+", b, "=", result)

result = a - b
print(a, "-", b, "=", result)
```

```python
C:\BigData\venv\Scripts\python.exe "C:/BigData/Code 03-03 계산기1.py"
숫자 1-->55
숫자 2-->44
55 + 44 = 99
55 - 44 = 11

Process finished with exit code 0
```

* input()은 무조건 값을 문자열로 인식한다. 그래서 겉에 int()를 씌워줌
* 문자열끼리 더하면 그냥 이어준다. 문자열끼리 빼기는 안됨.



## print함수

```python
>>> print("%d %d" % (100,200)) # 괄호 안의 값을 그대로 앞의 서식에 대입해준다
100 200
>>> print("%f %f" % (100, 200)) # 괄호 안의 값을 그대로 앞 서식에 대입해 실수로 표시
100.000000 200.000000
>>> print("{} {}".format(100,200))
100 200
>>> print("{0} {1}".format(100,200)) # 괄호 안의 값 첫번째(0), 두번째(1)를 표시한다
100 200
>>> print("{1} {0}".format(100,200))
200 100
>>> print("{1:d} {0:f}".format(100,200)) # 괄호 안의 값을 특정 타입으로 표시한다
200 100.000000
>>> print("안녕? \n하세요") # \n은 줄바꿈
안녕? 
하세요
```

* **print는 표현방식만 바꾸는거지 값을 건드리지는 않는다.**
* %d: 정수 (Decimal)
* %f: 실수 (Float)

* 따옴표 속에 들어가는 서식(%d 등)과 따옴표 뒤에 나오는 숫자 또는 문자의 개수는 같아야 한다.



## 산술연산자

```python
>>> a=100
>>> a=a+1
>>> a
101
>>> a+=1
>>> a
102
>>> a=+1
>>> a
1
```



## 동전 교환

```python
## 함수 선언부 ##



## 변수 선언부 ##
money, c500, c100, c50, c10 = [0] * 5     # 돈, 동전 500, 동전 100, 동전 50, 동전 10.

# 변수 이름은 이름만 보고도 예측이 되게끔, 너무 짧지도 길지도 않게 만드는게 좋다
# 좋은 코드는 남들이 잘 알아보는 코드 - 1) 주석을 많이 달아라, 2) 범용적으로 (남들도 알아보기 쉽게) 짜라



## 메인 코드부 ##
if __name__ == '__main__':
    money = int(input("바꿀 돈 --> "))
    c500 = money // 500
    money %= 500
    c100 = money // 100
    money %= 100
    c50 = money // 50
    money %= 50
    c10 = money // 10
    money %= 10

    print("500원: ", c500, ", 100원: ", c100, ", 50원: ", c50, ", 10원: ", c10, ", 나머지: ", money)
```



## 3일차 퀴즈 3

Q3. 입력한 돈을 최소한의 지폐~동전까지 바꾸기

```python
## 변수 선언부 ##
money, b50000, b10000, b5000, b1000, c500, c100, c50, c10 = [0] * 9

## 메인 코드부 ##
if __name__=="__main__":
    money = int(input("바꿀 돈 --> "))
    b50000 = money // 50000
    money %= 50000
    b10000 = money // 10000
    money %= 10000
    b5000 = money // 5000
    money %= 5000
    b1000 = money // 1000
    money %= 1000
    c500 = money // 500
    money %= 500
    c100 = money // 100
    money %= 100
    c50 = money // 50
    money %= 50
    c10 = money // 10
    money %= 10

    print("5만원: ", b50000, ", 만원: ", b10000, ", 오천원: ", b5000, ", 천원: ", b1000, ", 500원: ", c500, ", 100원: ", c100, ", 50원: ", c50, ", 10원: ", c10, ", 나머지: ", money)
```



## if문 응용

```python
import random

numbers = []    # 비어있는 리스트

for _ in range(0,10):    # for (i=0; i<10; i++)
    numbers.append(random.randint(0,9))
print(numbers)

for num in range(0,10):
    if num not in numbers:
        print(num, "없어요")
```



## for문 1

```python
### 1부터 100까지 합계
hap = 0
for i in range(0,101,1): # 는 range(0,101)과 같고 이건 range(101)과 같다
    hap += i
print(hap)
```



## 3일차 퀴즈 4

Q4-1. 1부터 100까지 홀수의 합계
Q4-2. 1부터 100까지 7의 배수의 합계
Q4-3. 12345부터 100000까지 7878의 배수의 합계

```python
# 4-1
hap = 0
for i in range(1,101,2):
    hap += i
print(hap)

# 4-2
hap = 0
for i in range(7,101,7):
    hap += i
print(hap)

# 4-3
hap = 0
for i in range (12345, 100001,1):
    if i % 7878 == 0:
        hap += i
print(hap)
```



## while문 1

```python
hap = 0

for i in range(101):
    hap += i
print(hap)
```

while문은 참인 동안에 반복되는 것.

위 코드랑 똑같은 코드를  while문으로 작성해보면 다음과 같다.

```python
i=0
while i < 101 :
    hap += i
    i += 1
print(hap)
```

이번엔 1부터 더하다가 10000을 넘을 때 멈추고 싶다면 다음과 같이 쓴다.

```python
i = 0
while True:
    hap += i
    if hap > 10000:
        break
    i += 1
print(hap)
```



## Lotto 추첨

```python
import random



## 전역 변수 (Global variable) 선언부 ##
num = 0
lotto = []



## 메인 코드부 ##
if __name__ == '__main__':
    while True:
        num = random.randint(1,45)
        if num in lotto:
            pass
        else:
            lotto.append(num)
        if len(lotto) >= 6:
            break
    lotto.sort()
    print("축하합니다 --> ", lotto)
```



# Python에서 Database 관리 2

## MySQL 데이터 입력

```python
import pymysql

conn = pymysql.connect(host="192.168.56.107", user="root", password="1234", db="samsongDB", charset="utf8") # 1. DB 연결
cur = conn.cursor() # 2. 커서 생성 (트럭, 연결로프)
sql = "CREATE TABLE IF NOT EXISTS userTable2(userId INT, userName CHAR(5))"
cur.execute(sql)

sql = "INSERT INTO userTable2 VALUES(1, '홍길동')";
cur.execute(sql)
sql = "INSERT INTO userTable2 VALUES(2, '이순신')";
cur.execute(sql)

cur.close()
conn.commit()
conn.close() # 6. DB 닫기 (=연결 해제)
print ("OK~")
```



## MySQL 데이터 조회

```python
import pymysql

conn = pymysql.connect(host="192.168.56.107", user="root", password="1234", db="samsongDB", charset="utf8") # 1. DB 연결
cur = conn.cursor() # 2. 커서 생성 (트럭, 연결로프)
sql = "SELECT * FROM userTable2"
cur.execute(sql)

rows = cur.fetchall()

print(rows)

cur.close()
conn.close() # 6. DB 닫기 (=연결 해제)
print ("OK~")
```

