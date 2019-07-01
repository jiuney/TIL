### 퀴즈 1. AND 게이트를 훈련시키고 결과를 보자.

from sklearn import svm



clf = svm.SVC(gamma="auto")

clf.fit( [[0, 0],
          [0, 1],
          [1, 0],
          [1, 1]],
         [0, 0, 0, 1])

result = clf.predict([[1, 1]])
print(result)