from sklearn import svm, metrics



### 00. 훈련 데이터, 테스트 데이터 준비

train_data = [ [0, 0], [0, 1], [1, 0], [1, 1] ]     # 훈련 데이터
train_label = [0, 1, 1, 0]    # 훈련 데이터의 정답(을 label이라 함)
test_data = [[1, 0], [0, 0]]
test_label = [1, 0]



### 01. Classifier 생성(선택) --> 머신러닝 알고리즘 선택

clf = svm.NuSVC(gamma="auto")     # clf = classifier 약자    # svm에서 SVC 알고리즘을 쓰기로 선택한 것



### 02. 데이터로 학습 시키기

# clf.fit([훈련데이터], [정답])
clf.fit(train_data, train_label)



### 03. 정답률을 확인 (신뢰도)
result = clf.predict(test_data)
score = metrics.accuracy_score(result, test_label)
print("정답률: " + "{0:.2f}%".format(score*100))



### 04. 예측하기

# clf.predict([예측할 데이터])
result = clf.predict([[1, 0]])
print(result)