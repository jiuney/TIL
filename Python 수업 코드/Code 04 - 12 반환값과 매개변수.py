
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
