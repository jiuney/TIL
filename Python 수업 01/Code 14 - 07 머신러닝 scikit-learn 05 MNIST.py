from sklearn import svm, metrics
from sklearn.model_selection import train_test_split
import pandas as pd
import math
from sklearn.neighbors import KNeighborsClassifier



def changeValue(lst):
    # return [ float(v) / 255 for v in lst]
    return [math.ceil(float(v) / 255) for v in lst]

### 00. 훈련 데이터, 테스트 데이터 준비

csv = pd.read_csv("c:/BigData/MNIST/train_5k.csv")
train_data = csv.iloc[:, 1:].values
train_data = list(map(changeValue, train_data))
train_label = csv.iloc[:, 0].values
csv2 = pd.read_csv("c:/BigData/MNIST/t10k_0.5k.csv")
test_data = csv2.iloc[:, 1:].values
test_data = list(map(changeValue, test_data))
test_label = csv2.iloc[:, 0].values



### 01. Classifier 생성(선택) --> 머신러닝 알고리즘 선택

# clf = svm.NuSVC(gamma="auto")     # clf = classifier 약자    # svm에서 SVC 알고리즘을 쓰기로 선택한 것
clf = KNeighborsClassifier(3)



### 02. 데이터로 학습 시키기

# clf.fit([훈련데이터], [정답])
clf.fit(train_data, train_label)



### 03. 정답률을 확인 (신뢰도)
result = clf.predict(test_data)
score = metrics.accuracy_score(result, test_label)
print("정답률: " + "{0:.2f}%".format(score*100))



# # 그림 사진 보기
# import matplotlib.pyplot as plt
# import numpy as np
# img = np.array(test_data[0]).reshape(28, 28)
# plt.imshow(img, cmap="gray")
# plt.show()

### 04. 내꺼 예측하기

# # clf.predict([예측할 데이터])
# result = clf.predict([[4.6, 3.2, 2.1, 0.9]])
# print(result)