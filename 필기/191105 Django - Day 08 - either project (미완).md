# 0. 기본 설정

`django_crud2` 라는 폴더 생성. 이 안에서 모든 작업을 할 예정. `django_crud2` 폴더 내에서 vscode 열기.

가상환경 만들고 가상환경 내에 django 설치.

```bash
python -m venv venv
activate
pip install django
```

`crud` 프로젝트 만들고 앱 `eithers` 만들기.

```bash
django-admin startproject crud .
python manage.py startapp eithers
```

`crud` > `settings.py` 에 앱 추가하고, template 경로 수정하고, media 경로 만들기.

```python
...

INSTALLED_APPS = [
    'eithers',
    ...
]

...

TEMPLATES = [
    {
        ...
        'DIRS': [os.path.join(BASE_DIR, 'eithers', 'templates', 'eithers')],
        ...
    },
]

...

# 맨 밑에 추가
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

`crud` > `urls.py` 에 eithers 앱의 urls 추가해주고 media파일들 경로도 추가해주기.

```python
...
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    ...
    path('eithers/', include('eithers.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

`eithers` > `templates` 폴더 생성 > `eithers` 폴더 생성 > `base.html` 생성.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Eithers Project</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
</head>
<body>
    
    <div class="container">
        {% block content %}
        {% endblock %}
    </div>

    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
</body>
</html>
```

`eithers` > `urls.py` 생성.

```python
from django.urls import path
from . import views

app_name = 'eithers'

urlpatterns = [
    path('', views.index, name="index"),
]
```

`eithers` > `views.py`

```python
...

def index(request):
    return render(request, 'eithers/index.html')
```

`eithers` > `templates` > `eithers` > `index.html` 생성.

```html
<!-- eithers/index.html -->

{% extends 'base.html' %}

{% block content %}

    <h1>Hello!</h1>

{% endblock %}
```

pillow 설치.

```bash
pip install Pillow
```

`eithers` > `models.py` 작성.

```python
class Question(models.Model):
    title = models.CharField(max_length=50)
    issue_a = models.CharField(max_length=200)
    issue_b = models.CharField(max_length=200)
    image_a = models.ImageField(blank=True, upload_to="eithers/images")
    image_b = models.ImageField(blank=True, upload_to="eithers/images")

class Answer(models.Model):
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    pick = models.IntegerField()
    comment = models.TextField()
```

수정한 모델 migrate.

```bash
python manage.py makemigrations
python manage.py migrate
```

관리자계정(superuser) 만들기.

```bash
python manage.py createsuperuser
```

관리자 페이지에 `eithers` 앱 표시하기: `eithers` > `admin.py` 수정.

```python
from django.contrib import admin
from .models import Question, Answer

# Register your models here.

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'issue_a', 'issue_b', 'image_a', 'image_b')

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('pk', 'question_id', 'pick')

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
```



# 1. 새 글 작성하기

`eithers` > `urls.py`

```python
urlpatterns = [
    ...
    path('create/', views.create, name="create"),
]
```

`eithers` > `views.py`

```python
def create(request):
    if request.method == "POST":
        pass
    else:
        return render(request, 'eithers/new.html')
```

`eithers` > `templates` > `eithers` > `new.html` 생성.

```html
<!-- eithers/new.html -->

{% extends 'base.html' %}

{% block content %}

<form action="{% url 'eithers:create' %}" method="POST" enctype="multipart/form-data">
    {% csrf_token %}
    <div class="form-group">
        <label for="title">제목</label>
        <input type="text" class="form-control" id="title" name="title" placeholder="글 제목을 입력해주세요.">
    </div>
    <div class="form-group">
        <label for="issue_a">첫번째 선택지</label>
        <input type="text" class="form-control" id="issue_a" name="issue_a" placeholder="첫번째 선택지를 입력해주세요.">
    </div>
    <div class="custom-file">
        <input type="file" class="custom-file-input" id="image_a" name="image_a">
        <label class="custom-file-label" for="image_a">첫번째 선택지의 이미지를 업로드하세요.</label>
    </div>
    <br>
    <br>
    <div class="form-group">
        <label for="issue_b">두번째 선택지</label>
        <input type="text" class="form-control" id="issue_b" name="issue_b" placeholder="두번째 선택지를 입력해주세요.">
    </div>
    <div class="custom-file">
        <input type="file" class="custom-file-input" id="image_b" name="image_b">
        <label class="custom-file-label" for="image_b">두번째 선택지의 이미지를 업로드하세요.</label>
    </div>
    <br>
    <br>
    <button type="submit" class="btn btn-primary">Submit</button>
</form>

{% endblock %}
```

`eithers` > `views.py`

```python
...
from .models import Question, Answer

...

def create(request):
    if request.method == "POST":
        title = request.POST.get('title')
        issue_a = request.POST.get('issue_a')
        issue_b = request.POST.get('issue_b')
        image_a = request.FILES.get('image_a')
        image_b = request.FILES.get('image_b')
        Question.objects.create(
            title = title,
            issue_a = issue_a,
            issue_b = issue_b,
            image_a = image_a,
            image_b = image_b
        )
        return redirect('eithers:index')
    else:
        return render(request, 'eithers/new.html')
```



# 2. 상세 페이지 만들기

`eithers` > `urls.py`

```python
urlpatterns = [
    ...
    path('<int:question_pk>/', views.detail, name="detail"),
]
```

`eithers` > `views.py`

```python
def detail(request, question_pk):
    question = Question.objects.get(pk=question_pk)
    context = {
        'question': question
    }
    return render(request, 'eithers/detail.html', context)
```

`eithers` > `templates` > `eithers` > `detail.html` 생성.

```html
<!-- eithers/detail.html -->

{% extends 'base.html' %}

{% block content %}

<h3 class="text-center">{{ question.title }}</h3>
<br>
<div class="row">
    <div class="col-sm-6">
        <div class="card">
            <img src="{{ question.image_a.url }}" class="card-img-top" alt="...">
            <div class="card-body">
                <h5 class="card-title text-center">{{ question.issue_a }}</h5>
            </div>
        </div>
    </div>
    <div class="col-sm-6">
        <div class="card">
            <img src="{{ question.image_b.url }}" class="card-img-top" alt="...">
            <div class="card-body">
                <h5 class="card-title text-center">{{ question.issue_b }}</h5>
            </div>
        </div>
    </div>
</div>

{% endblock %}
```



# 3. 첫 페이지 수정

`eithers` > `templates` > `eithers` > `base.html` 에 navigation bar 넣기.

```html
...
<body>
    ...
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <a class="navbar-brand" href="{% url 'eithers:index' %}">Eithers</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav mr-auto">
                <li class="nav-item">
                    <a class="nav-link" href="{% url 'eithers:create' %}">New Issue</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="#">Random</a>
                </li>
            </ul>
            <form class="form-inline my-2 my-lg-0">
                <input class="form-control mr-sm-2" type="search" placeholder="Search" aria-label="Search">
                <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
            </form>
        </div>
    </nav>
    ...
</body>
</html>
```

`eithers` > `templates` > `eithers` > `index.html` 수정.

```html
<!-- eithers/index.html -->

{% extends 'base.html' %}

{% block content %}

<ul class="list-group list-group-flush">
    {% for question in questions %}
        <a href="{% url 'eithers:detail' question.pk %}" style="text-decoration: none !important;">
            <li class="list-group-item list-group-item-action">{{ question.title }}</li>
        </a>
    {% endfor %}
</ul>

{% endblock %}
```

`eithers` > `views.py` 에서 index 메소드 수정.

```python
def index(request):
    questions = Question.objects.all()
    context = {
        'questions': questions
    }
    return render(request, 'eithers/index.html', context)
```



# 4. Answer 기능 넣기



## 0) 최신 게시물/답변이 가장 먼저 출력되게 모델 수정

`eithers` > `models.py` 에서 Answer 클래스 수정.

```python
class Question(models.Model):
    ...

    class Meta:
        ordering = ['-pk']

class Answer(models.Model):
    ...

    class Meta:
        ordering = ['-pk']
```



## 1) 상세 페이지에서 답변 보이게 하기

우선 답변이 보여야 하니까 예시로 하나 만들 것.

shell plus를 사용하기 위해 django-extension 설치.

```bash
pip install django-extensions
```

`crud` > `settings.py` 에 앱 추가.

```python
INSTALLED_APPS = [
    ...
    'django_extensions',
]
```

shell plus 실행.

```bash
python manage.py shell_plus
```

답변 하나 만들기.

```python
>>> question = Question.objects.get(pk=2)
>>> answer = Answer()
>>> answer.question_id = question
>>> answer.pick = 2
>>> answer.comment = "펭수가 대세지."
>>> answer.save()
```

`eithers` > `views.py` 에서 detail 메소드 수정.

```python
def detail(request, question_pk):
    question = Question.objects.get(pk=question_pk)
    answers = Answer.objects.filter(question_id=question)
    context = {
        'question': question,
        'answers': answers
    }
    return render(request, 'eithers/detail.html', context)
```

`eithers` > `templates` > `eithers` > `detail.html` 수정.

```html
<!-- eithers/detail.html -->

...

<div class="row">
    ...
</div>

<hr>
답변 입력 자리
<hr>

<ul class="list-group list-group-flush">
    {% for answer in answers %}
        <li class="list-group-item list-group-item-action" style="
            color: 
                {% if answer.pick == 1 %}
                    Orange
                {% elif answer.pick == 2 %}
                    Purple
                {% endif %};">
            {{ answer.comment }}
        </li>
    {% endfor %}
</ul>

{% endblock %}
```



## 2) 답변 입력 기능 넣기

`eithers` > `templates` > `eithers` > `detail.html` 에서 "답변 입력 자리"에 다음 코드 넣기. ===== 아직 미완!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

```html
<!-- eithers/detail.html -->

...

<hr>

<form class="was-validated">

    <div class="form-group">
        <select class="custom-select" required>
            <option value="">당신의 선택은?</option>
            <option value="1">{{ question.issue_a }}</option>
            <option value="2">{{ question.issue_b }}</option>
        </select>
        <div class="invalid-feedback">반드시 하나를 선택하셔야 합니다.</div>
    </div>

    <div class="mb-3">
        <label for="validationTextarea">선택 이유</label>
        <textarea class="form-control is-invalid" id="validationTextarea" placeholder="왜 선택하셨나요?" required></textarea>
        <div class="invalid-feedback">
            이유가 꼭 필요해요.
        </div>
    </div>

    <button class="btn btn-light" type="submit">Submit</button>

</form>

<hr>

...
```

