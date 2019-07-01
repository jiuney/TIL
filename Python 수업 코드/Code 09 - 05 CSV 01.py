import csv

# with open("C:/images/csv/emp.csv") as rfp:
#     while True:
#         line = rfp.readline()
#         if not line:
#             break
#         print(line)

# ## 우리회사 연봉 평균은?
# with open("C:/images/csv/emp.csv") as rfp:
#     sum = 0
#     line = rfp.readline()    # 첫번째 줄은 데이터가 아니므로 여기서 읽고 버린다
#     count = 0
#     while True:
#         line = rfp.readline()
#         if not line:
#             break
#         count += 1
#         lineList = line.split(",")
#         sum += int(lineList[3])
#     avg = sum // count
#     print(avg)

## 우리회사 연봉 평균은?
with open("C:/images/csv/emp.csv") as rfp:
    reader = csv.reader(rfp)
    headerList = next(reader)
    sum = 0
    count = 0
    for cList in reader:
        # print(cList)
        sum += int(cList[3])
        count += 1
    avg = sum // count
    print(avg)