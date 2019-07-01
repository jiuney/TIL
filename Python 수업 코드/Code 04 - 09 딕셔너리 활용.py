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
