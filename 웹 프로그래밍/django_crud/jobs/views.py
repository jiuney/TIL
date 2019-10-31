from django.shortcuts import render
from .models import Job
from faker import Faker
import requests
from decouple import config

# Create your views here.

def index(request):
    return render(request, 'jobs/index.html')

def past_life(request):
    name = request.POST.get("name")

    # db에 이름이 있는지 확인
    try:
        check = Job.objects.get(name=name)
    except:
        check = 0

    # db에 이미 같은 name이 있으면 기존 name의 past_job 가져오기
    if check != 0:
        past_job = check.past_job

    # 없으면 db에 저장한 후 가져오기
    if check == 0:
        fake = Faker()
        fakejob = fake.job()
        Job.objects.create(name=name, past_job=fakejob)
    
    check = Job.objects.get(name=name)
    past_job = check.past_job

    GIPHY_API_KEY = config("GIPHY_API_KEY")
    url = f'http://api.giphy.com/v1/gifs/search?api_key={GIPHY_API_KEY}&q={past_job}'
    data = requests.get(url).json()
    # gif_url = data["data"][0]["images"]["original"]["url"] # 근데 이렇게 하면 KEY가 없을 경우 에러가 발생한다
    # 강사님 코드
    gif_url = data.get("data")[0].get("images").get("original").get("url")
    # 강사님 코드대로 쓰면 KEY가 없을 경우에도 에러가 뜨지 않고 None값을 가져오게 된다.

    context = {
        'name': name,
        'pastjob': past_job,
        'gif_url': gif_url
    }

    return render(request, 'jobs/past_life.html', context)

''' 강사님 코드
def past_life(request):
    name = request.POST.get("name")

    # db에 이름이 있는지 확인
    person = Job.objects.filter(name=name).first()

    # db에 이미 같은 name이 있으면 기존 name의 past_job 가져오기
    if person:
        past_job = person.past_job

    # 없으면 db에 저장한 후 가져오기
    else:
        faker = Faker('ko-KR')
        past_job = faker.job()
        person = Job(name=name, past_job=past_job)
        person.save()

    context = {
        'name': person.name,
        'pastjob': person.past_job
    }

    return render(request, 'jobs/past_life.html', context)
'''

