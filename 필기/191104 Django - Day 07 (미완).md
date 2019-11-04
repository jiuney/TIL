

html css javascript image 등 전부 다 = static

static file = django가 기본적으로 가지고 있는 것

media file = 사용자가 올리는 것







mkdir django_statics

cd django_statics

python -m venv venv

activate

pip install django

django-admin startproject django_statics .

python manage.py startapp articles

settings.py 앱 추가 템플릿 디렉토리 추가

```python
INSTALLED_APPS = [
    'articles',
    ...
]

TEMPLATES = [
    {
        ...
        'DIRS': [os.path.join(BASE_DIR, 'django_statics', 'templates')],
        ...
    },
]
```



프로젝트 폴더에 templates > base.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Django Static!</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
</head>
<body>

    <div class="container">
            {% block body %}
            {% endblock %}
    </div>

    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>    
</body>
</html>
```



urls.py

```python
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('articles/', include('articles.urls'))
]
```

articles > urls.py

```python
from django.urls import path
from . import views

app_name = "articles"

urlpatterns = [
    path('', views.index, name="index")
]
```

views.py

```python
def index(request):
    return render(request, 'articles/index.html')
```

프로젝트폴더 settings.py

```python
STATIC_URL = '/static/'
```

* template 파일을 찾을 때 기본적으로 templates 폴더를 찾는것처럼, static file을 찾을 때 기본적으로 static 폴더를 찾게 된다.



articles 밑에 static > articles 폴더 생성, 그 밑에 이미지 파일 넣기

index.html

```html
<!-- articles/index.html -->

{% extends 'base.html' %}
{% load static %}

{% block body %}

    <h1>Articles!</h1>
    <img src="{% static 'articles/penghi.jpg' %}" alt="peng-hi!">

{% endblock %}
```

* {% load static %} 으로 static 폴더 경로를 바로 불러올 수 있다



스태틱 파일 기본경로를 따로 지정해줄 수도 있다

프로젝트폴더 settings.py 맨 밑에 다음 코드 추가

```python
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'my_images'),
]
```



manage.py랑 같은 레벨에 my_images 폴더 생성



my_images 폴더 안에 이미지 넣기

index.html

```html
<!-- articles/index.html -->

{% extends 'base.html' %}
{% load static %}

{% block body %}

    <h1>Articles!</h1>
    <img src="{% static 'articles/penghi.jpg' %}" alt="peng-hi!"><br>
    <img src="{% static 'strawberry.jpg' %}" alt="strawberry">

{% endblock %}
```







========= 사용자로부터 이미지 받기 =========

articles > models.py

```python

```

* imagefield는 이미지를 데이터베이스에 넣는게 아니라 해당 이미지의 경로를 저장하게 된다.
* blank=True는 사용자로부터 입력을 굳이 받지 않아도 된다는 의미

* 근데 이미지필드는 pillow가 설치되어 있어야 한다.



```bash
pip install pillow

python manage.py makemigrations
python manage.py migrate
```



게시물 만드는 로직 만들 것



articles > views.py

```python
from django.shortcuts import render, redirect

...

def create(request):
    if request.method == "POST":
        return redirect('articles:index')
    else:
        return render(request, 'articles/create.html')
```



articles > create.html

```html
<!-- articles/create.html -->

{% extends 'base.html' %}

{% block body %}

    <form action="{% url 'articles:create' %}" method="POST">
        {% csrf_token %}
        <input type="text" name="title"><br>
        <input type="text" name="content"><br>
        <input type="file" name="image"><br>
        <input type="submit">
    </form>

{% endblock %}
```

* create 메소드가 자기한테서 왔기 때문에 form태그에 action 주소를 안써주면 submit한 정보가 다시 자신에게 온다.
  * 그래도 명시적으로 써주는게 좋다



articles > urls.py

```python
urlpatterns = [
    ...
    path('create/', views.create, name="create"),
]
```



views.py

```python
from .models import Article

...

def create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        image = request.FILES.get("image")
        article = Article(
            title=title,
            content=content,
            image=image
        )
        article.save()
        return redirect('articles:index')
    else:
        return render(request, 'articles/create.html')
```

* 이미지 파일은 request.FILES.get 으로 가져와야 한다



articles > admin.py

```python
from django.contrib import admin
from .models import Article

# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'content', 'image', 'created_at', 'updated_at')

admin.site.register(Article, ArticleAdmin)
```



superuser 만들기

```bash
python manage.py createsuperuser
```



근데 create 페이지에서 이미지 접수하고 관리자 페이지 확인하면 title이랑 content는 있는데 이미지는 없다

create.html에서 다음과 같이 써줘야 함

```html
<!-- articles/create.html -->

{% extends 'base.html' %}

{% block body %}

    <form action="{% url 'articles:create' %}" method="POST" enctype="multipart/form-data">
        {% csrf_token %}
        <input type="text" name="title"><br>
        <input type="text" name="content"><br>
        <input type="file" name="image"><br>
        <input type="submit">
    </form>

{% endblock %}
```

* form태그에 옵션으로 `enctype="multipart/form-data"` 를 넣어줘야 함











========= 입력한 이미지 출력 =========



articles > views.py

```python
def detail(request, pk):
    article = Article.objects.get(pk=pk)
    context = {
        'article': article
    }
    return render(request, 'articles/detail.html', context)
```



articles > urls.py

```python
urlpatterns = [
    ...
    path('<int:pk>/', views.detail, name="detail"),
]
```



articles > detail.html

```html
<!-- articles/detail.html -->

{% extends 'base.html' %}

{% block body %}

    <h1>{{ article.title }}</h1>
    <p>{{ article.content }}</p>
    {% if article.image %}
        <p><img src="{{ article.image.url }}" alt="image"></p>
    {% endif%}

{% endblock %}
```



근데 여전히 이미지를 못가져온다.



프로젝트 폴더의 settings.py에서 맨 마지막에 추가

```python
# STATIC_URL과 비슷. 업로드 된 파일의 주소를 만들어준다.
# 실제 업로드 된 파일의 경로를 의미하는 것은 아니다.

MEDIA_URL = '/media/'

# 업로드 된 파일을 저장하는 경로

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

* BASE_DIR에 media 폴더가 없으면 생성해서 저장하게 된다



프로젝트 폴더의 urls.py에

```python
...
from django.conf import settings
from django.conf.urls.static import static

...

urlpatterns = [
    ...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```



views.py에 index 수정

```python
def index(request):
    articles = Article.objects.all()
    context = {
        'articles': articles
    }
    return render(request, 'articles/index.html', context)
```



index.html도 수정해준다

```html
<!-- articles/index.html -->

{% extends 'base.html' %}
{% load static %}

{% block body %}

    <h1>Articles!</h1>
    <hr>
    {% for article in articles %}

        <h3><a href="{% url 'articles:detail' article.pk %}">{{ article.title }}</a></h3>
        <p>{{ article.content }}</p>

        {% if article.image %}

            <p><img src="{{ article.image.url }}" alt="image"></p>

        {% endif%}

        <hr>

    {% endfor %}

{% endblock %}
```



============= 업데이트 기능 만들기 =============

urls.py

```python
urlpatterns = [
    ...
    path('<int:pk>/update/', views.update, name="update"),
]
```



detail.html 수정버튼 만들기

```html
<!-- articles/detail.html -->

{% extends 'base.html' %}

{% block body %}

    <h1>{{ article.title }}</h1>
    <p>{{ article.content }}</p>
    {% if article.image %}
        <p><img src="{{ article.image.url }}" alt="image"></p>
    {% endif%}
    <a href="{% url 'articles:update' article.pk %}">[ 수정 ]</a>

{% endblock %}
```



views.py

```python
def update(request, pk):
    article = Article.objects.get(pk=pk)

    if request.method == "POST":
        article.title = request.POST.get("title") or article.title
        article.content = request.POST.get("content") or article.content
        article.image = request.FILES.get("image") or article.image
        article.save()
        return redirect('articles:detail', article.pk)
    else:
        context = {
            'article': article
        }
        return render(request, 'articles/update.html', context)
```

* or을 쓰면, 전자가 빈칸으로 온다면 뒤에가 들어간다는 뜻



update.html

```html
<!-- articles/update.html -->

{% extends 'base.html' %}

{% block body %}

    <form action="{% url 'articles:update' article.pk %}" method="POST" enctype="multipart/form-data">
        {% csrf_token %}
        <input type="text" name="title" placeholder="{{ article.title }}"><br>
        <input type="text" name="content" placeholder="{{ article.content }}"><br>
        <input type="file" name="image"><br>
        <input type="submit" value="수정">
    </form>

{% endblock %}
```

* value는 값이 들어가는거고 placeholder는 값은 비어있다 (안내문구만 뜨는 것)
  * value는 아무것도 입력하지 않고 submit하면 value에 들어있던 값이 submit되고, placeholder는 아무것도 입력하지 않고 submit하면 아무것도 submit되지 않는다.



======= 미디어 파일 저장 경로 수정 =======

articles > models.py

```python
from django.db import models

def articles_image_path(instance, filename):
    # return f'articles/{instance.pk}번글/images/{filename}'
    # 그런데 위와 같이 하면 instance가 없는 경우 instance.pk가 0이 될 수 있어 좋은 practice가 아니라고 함.
    # 그래서 django에서 권장하는 저장경로는 다음과 같음.
    return f'articles/%Y/%m/%d'
    # 근데 함수로 만들면 위와 같은 parsing이 안먹힘;;
    # 그래서 강사님께서 그냥 아래처럼 upload_to 다음에 경로 쓰라고 하심.

# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(blank=True, upload_to="articles/%Y/%m/%d")    # ImageField는 pillow 필수
```



============ 삭제 버튼 만들기 ============

urls.py

```python
urlpatterns = [
    ...
    path('<int:pk>/delete/', views.delete, name="delete"),
]
```



views.py

```python
def delete(request, pk):
    article = Article.objects.get(pk=pk)
    article.delete()
    return redirect('articles:index')
```



detail.html

```html
...
<form action="{% url 'articles:delete' article.pk %}" method="POST">
    {% csrf_token %}
    <input type="submit" value="삭제" onclick="return confirm('삭제하시겠어요?')">
</form>
...
```



============ 게시물 삭제했을 때 파일까지 지우기 ============

views.py

```python
def delete(request, pk):
    article = Article.objects.get(pk=pk)
    article.image.delete()   # 이거 추가
    article.delete()
    return redirect('articles:index')
```

* 근데 반드시 delete() 전에 image.delete()를 먼저 해야 한다









============ bootstrap으로 다듬어보기 ============

index.html

```html
<!-- articles/index.html -->

{% extends 'base.html' %}
{% load static %}

{% block body %}

    <h1>Articles!</h1>
    <hr>

    <ul class="list-unstyled ">
        {% for article in articles %}
            <li class="media">
                
                {% if article.image %}
                    <img src="{{ article.image.url }}" class="mr-3" alt="..." width="64">
                {% else %}
                    <img src="..." class="mr-3" alt="..." width="64">
                {% endif %}

                <div class="media-body mb-5">
                    <h5 class="mt-0 mb-1 "><a href="{% url 'articles:detail' article.pk %}" class="list-group-item-action list-group-flush">{{ article.title }}</a></h5>
                    {{ article.content }}
                </div>
            </li>
        {% endfor %}
    </ul>

{% endblock %}
```































































































