import numpy as np

list2 = [num for num in range(10, 100, 10)]

A = np.array(list2)

myList = [[n for n in range (10, 50, 10)] for _ in range (10, 50, 10)]

B = np.array(myList)

myList + 100    # 안된다

B + 100    # 된다




















