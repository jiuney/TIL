# 1. 파일 열기
inFp = open('c:/windows/win.ini', 'r')
outFp = open('c:/images/new_win.ini', 'w')
# 2. 파일 읽기/쓰기
while True :
    inStr = inFp.readline()
    if not inStr:
        break
    outFp.writelines(inStr)
# inStrList = inFp.readlines()
# print(inStrList)
# for  line in inStrList :
#     print(line, end='')

# 3. 파일 닫기
inFp.close()
outFp.close()
print('OK~')