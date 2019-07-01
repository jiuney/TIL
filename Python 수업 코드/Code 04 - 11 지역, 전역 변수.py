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