
hap = 0

# for i in range(101):
#     hap += i
# print(hap)

# 위 코드랑 똑같은 코드를 while문으로 작성해보기
# while문은 참인 동안에 반복되는 것

# i=0
# while i < 101 :
#     hap += i
#     i += 1
# print(hap)


# 1부터 더하다가 10000을 넘을 때 멈추고 싶다
i = 0
while True:
    hap += i
    if hap > 10000:
        break
    i += 1
print(hap)