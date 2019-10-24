from django.shortcuts import render
import random
import math
from datetime import datetime

# Create your views here.

def index(request):
    return render(request, 'pages/index.html')    # 경로에서 templates는 django가 알아서 잡아준다.

def introduce(request, name, age):
    context = {
        'name': name,
        'age': age
    }
    return render(request, 'pages/introduce.html', context)

def dinner(request):
    menu = ['김치찌개', '순두부찌개', '짜장면', '햄버거', '치킨', '초밥', '김밥']
    pick = random.choice(menu)
    # return render(request, 'pages/dinner.html', {'pick': pick})    # pick을 넘겨주기 위해 dictionary 형태로 써준다
    context = {'pick': pick}    # 넘겨줘야 할 딕셔너리를 따로 변수에 담아주면 넘겨 줄 딕셔너리를 관리하기 용이해진다.
    return render(request, 'pages/dinner.html', context)

def image(request):
    return render(request, 'pages/image.html')

def hello(request, name):
    menu = ['김치찌개', '순두부찌개', '짜장면', '햄버거', '치킨', '초밥', '김밥']
    pick = random.choice(menu)
    context = {
        'name': name,
        'pick': pick
    }
    return render(request, 'pages/hello.html', context)

def times(request, num1, num2):
    result = num1 * num2
    context = {
        'num1': num1,
        'num2': num2,
        'result': result
    }
    return render(request, 'pages/times.html', context)

def circle(request, radius):
    area = math.pi * (radius ** 2)
    context = {
        'radius': radius,
        'area': area
    }
    return render(request, 'pages/circle.html', context)

def template_language(request):
    menus = ['김치찌개', '순두부찌개', '짜장면', '햄버거', '치킨', '초밥', '김밥']
    my_sentence = "Life is short, you need python."
    messages = ['apple', 'banana', 'cucumber', 'mango']
    datetimenow = datetime.now()
    empty_list = []
    context = {
        'menus': menus,
        'my_sentence': my_sentence,
        'messages': messages,
        'datetimenow': datetimenow,
        'empty_list': empty_list
    }
    return render(request, 'pages/template_language.html', context)

'''
실습 #1.
오늘이 내 생일이면 "예", 아니면 "아니요"를 화면에 띄워주세요.
DTL (Django Template Language) 를 이용해주세요!
'''
def isbirth(request):
    birthday = datetime(2000, 10, 24)
    today = datetime.today()
    context = {
        'birthday_month': birthday.month,
        'birthday_day': birthday.day,
        'today_month': today.month,
        'today_day': today.day
    }
    return render(request, 'pages/isbirth.html', context)

'''
실습 #2.
url을 통해 들어오는 문자열이 회문(palindrome)인지 아닌지를 판별해주세요!
'''
def ispal(request, input):
    for i in range(len(input)//2):
        if input[i] == input[-(i+1)]:
            answer = "회문이 맞습니다."
        else:
            answer = "회문이 아닙니다."
    # if input == input[::-1]:
    #     answer = "회문이 맞습니다."
    # else:
    #     answer = "회문이 아닙니다."
    context = {
        'input': input,
        'answer': answer
    }
    return render(request, 'pages/ispal.html', context)