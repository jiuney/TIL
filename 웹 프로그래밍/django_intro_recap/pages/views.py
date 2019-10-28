from django.shortcuts import render
import random
import requests

# Create your views here.

def index(request):
    return render(request, 'pages/index.html')

# throw & catch 연습
def throw(request):
    return render(request, 'pages/throw.html')
def catch(request):

    print("START"+"-"*30)
    print(request)
    print("-"*30)
    print(request.scheme)
    print("-"*30)
    print(request.path)
    print("-"*30)
    print(request.method)
    print("-"*30)
    print(request.headers)
    print("-"*30)
    print(request.META)
    print("-"*30)
    print(request.GET)
    print("-"*30+"END")

    message = request.GET.get("message")
    message2 = request.GET.get("message2")
    context = {
        'message': message,
        'message2': message2
    }
    return render(request, 'pages/catch.html', context)

# 로또 번호 추첨
def lotto_pick(request):
    return render(request, 'pages/lotto_pick.html')
def lotto_get(request):
    lottos = range(1, 46)
    pick = random.sample(lottos, 6)
    name = request.GET.get("name")
    context = {
        'name': name,
        'pick': pick
    }
    return render(request, 'pages/lotto_get.html', context)
def lottery(request):
    return render(request, 'pages/lottery.html')
def jackpot(request):
    
    # 1. 사용자의 이름을 받아오자.
    name = request.GET.get("name")
    ep = request.GET.get("ep")
    
    # 2. 나눔로또 API로 요청을 보내 결과 받기.
    res = requests.get(f"https://dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={ep}")
    res = res.json()
    
    # 3. 로또 당첨번호 6개를 골라 winner 리스트에 담자!
    winner = []
    for i in range(1, 7):
        winner.append(res[f'drwtNo{i}'])
    
    # 4. 1~45까지의 수 중에서 6개를 뽑아 리스트에 담자
    pick = random.sample(range(1,46), 6)
    pick = sorted(pick)

    # 5. set를 활용해 교집합 연산을 활용, 실제 로또 당첨 번호와 컴시기가 뽑아준 번호의 개수 구하기
    lotto_res = set(winner) & set(pick)
    resNo = len(lotto_res)

    # 6. 매칭 결과에 따라 다른 응답 메세지 나타내기 (보너스 번호 제외)
    if resNo == 6:
        message = "1등"
    elif resNo == 5:
        message = "2등"
    elif resNo == 4:
        message = "3등"
    else:
        message = "꽝"

    # 7. 딕셔너리를 넘기자!
    context = {
        'name': name,
        'message': message,
        'winner': winner,
        'pick': pick,
        'match': list(zip(winner, pick))
    }

    return render(request, 'pages/jackpot.html', context)

# POST 연습
def user_new(request):
    return render(request, 'pages/user_new.html')
def user_create(request):
    name = request.POST.get("name")
    password = request.POST.get("password")
    context = {
        'name': name,
        'password': password
    }
    return render(request, 'pages/user_create.html', context)

def static_example(request):
    return render(request, 'pages/static_example.html')