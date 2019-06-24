from sklearn import svm, metrics
import pandas as pd



'''
# 붓꽃 데이터 분류기 (머신러닝)
- 개요: 150개 붓꽃 정보 (꽃받침 길이, 꽃받침 폭, 꽃잎 길이, 꽃잎 폭)
- 종류: 3개 (Iris-setosa, Iris-versicolor, Iris-virginica)
- CSV 파일: 검색
'''



### 00. 훈련 데이터, 테스트 데이터 준비

csv = pd.read_csv("c:/BigData/CSV/iris.csv")
train_data = csv.iloc[0:120, 0:-1]
train_label = csv.iloc[0:120, [-1]]
test_data = csv.iloc[120:, 0:-1]
test_label = csv.iloc[120:, [-1]]



### 01. Classifier 생성(선택) --> 머신러닝 알고리즘 선택

clf = svm.SVC(gamma="auto")     # clf = classifier 약자    # svm에서 SVC 알고리즘을 쓰기로 선택한 것



### 02. 데이터로 학습 시키기

# clf.fit([훈련데이터], [정답])
clf.fit(train_data, train_label)



### 03. 정답률을 확인 (신뢰도)
result = clf.predict(test_data)
score = metrics.accuracy_score(result, test_label)
print("정답률: " + "{0:.2f}%".format(score*100))



### 04. 내꺼 예측하기

# clf.predict([예측할 데이터])
result = clf.predict([[4.6, 3.2, 2.1, 0.9]])
print(result)