### 1부터 100까지 합계
hap = 0
for i in range(0,101,1): # 는 range(0,101)과 같고 이건 range(101)과 같다
    hap += i
print(hap)

'''
퀴즈 4-1. 1부터 100까지 홀수의 합계
퀴즈 4-2. 1부터 100까지 7의 배수의 합계
퀴즈 4-3. 12345부터 100000까지 7878의 배수의 합계
'''

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