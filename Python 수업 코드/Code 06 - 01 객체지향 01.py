class Car:
    # 자동차 속성
    color = None
    speed = 0
    # 자동차의 행위 (--> 함수, 기능)
    def upSpeed(self, value):
        self.speed += value    # 여기서 speed는 변수가 아니라 Car라는 클래스의 속성이므로 앞에 "self."를 붙인다.
    def downSpeed(self):
        self.speed -= value

#######################################

car1 = Car() ; car2 = Car()   # 여기서 car1, car2는 변수가 아니라 instance이다. instance는 클래스를 통해서 찍어내는 것.

car1.color = "빨강"
car1.speed = 50
car1.upSpeed(100)

print(car1.speed)

#######################################

from tkinter import *

button1 = Button()
