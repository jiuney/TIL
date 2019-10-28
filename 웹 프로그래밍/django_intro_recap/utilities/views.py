from django.shortcuts import render
import requests

# Create your views here.

def index(request):
    return render(request, 'utilities/index.html')

def asciify(request):
    return render(request, 'utilities/asciify.html')

def asciify2(request):
    return render(request, 'utilities/asciify2.html')

def asciify2_art(request):

    # 1. form 태그로 날린 데이터를 받는다 (GET 방식).
    engtext = request.GET.get("engtext")

    # 2. artii api로 요청을 보낸다.
    res = requests.get(f'http://artii.herokuapp.com/make?text={engtext}')
    art = res.text

    print("START"+"-"*30)
    print(art)
    print("-"*30+"END")

    context = {
        'art': art
    }
    return render(request, 'utilities/asciify2_art.html', context)