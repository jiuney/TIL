(수업 빠져서 [NoelBird님 필기](https://github.com/NoelBird/AI_multicampus/blob/master/8-Web/7%EC%9D%BC%EC%B0%A8/2019-10-30_REST.md) 따라함)



















========== detail 페이지 만들기 ==========



`django_crud` > `articles` > `urls.py`

```python
urlpatterns = [
    path('', views.index),
    path('new/', views.new),
    path('create/', views.create),
    path('detail/<int:pk>/', views.detail)    # 추가
]
```



`django_crud` > `articles` > `views.py`

```python
def detail(request, pk):
    article = Article.objects.get(pk=pk)
    context = {
        'article': article
    }
    return render(request, 'articles/detail.html', context)
```



`django_crud` > `articles` > `templates` > `articles` > `detail.html` 생성

```html
<!-- templates/articles/detail.html -->

{% extends 'base.html' %}

{% block content %}

    <h1 class="text-center">DETAIL</h1>
    <h2>{{ article.pk }}번째 글</h2>
    <hr>
    <p>{{ article.title }}</p>
    <p>{{ article.content }}</p>
    <p>{{ article.created_at | date:"SHORT_DATE_FORMAT" }}</p>
    <p>{{ article.updated_at | date:"M, j, Y" }}</p>
    <a href="/articles/">[BACK]</a>

{% endblock %}
```



========== 삭제 기능 만들기 ==========

`django_crud` > `articles` > `views.py`

```python
def delete(request, pk):
    article = Article.objects.get(pk=pk)
    article.delete()
    return redirect('/articles/')
```



`django_crud` > `articles` > `urls.py`

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('new/', views.new),
    path('create/', views.create),
    path('detail/<int:pk>/', views.detail),
    path('<int:pk>/delete/', views.delete)    # 여기 추가
]
```







========== 업데이트 기능 만들기 ==========





`django_crud` > `articles` > `urls.py`

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('new/', views.new),
    path('create/', views.create),
    path('detail/<int:pk>/', views.detail),
    path('<int:pk>/delete/', views.delete),
    path('<int:pk>/edit/', views.edit),    # 여기 추가
    path('<int:pk>/update/', views.update)    # 여기 추가
]
```



`django_crud` > `articles` > `views.py`

```python
def edit(request, pk):
    article = Article.objects.get(pk=pk)
    context = {
        'article': article
    }
    return render(request, 'articles/edit.html', context)

def update(request, pk):
    article = Article.objects.get(pk=pk)
    title = request.POST.get('title')
    content = request.POST.get('content')

    article.title = title
    article.content = content

    article.save()

    return redirect('/articles/')
```



수정하는 화면

`django_crud` > `articles` > `templates` > `articles` > `edit.html` 생성

```html
<!-- templates/articles/edit.html -->

{% extends 'base.html' %}

{% block content %}

    <h1 class="text-center">EDIT</h1>
    <form action="/articles/{{ article.pk }}/update/" method="POST">
        {% csrf_token %}
        <input type="text" name="title" value="{{ article.title }}"><br>
        <textarea name="content" id="" cols="30" rows="10">{{ article.content }}</textarea><br>
        <input type="submit" value="submit">
    </form>

{% endblock %}
```



edit/delete 할 수 있게 detail 페이지에 버튼 만들기

`django_crud` > `articles` > `templates` > `articles` > `detail.html` 

```html
<!-- templates/articles/detail.html -->

{% extends 'base.html' %}

{% block content %}

    <h1 class="text-center">DETAIL</h1>
    <h2>{{ article.pk }}번째 글</h2>
    <hr>
    <p>{{ article.title }}</p>
    <p>{{ article.content }}</p>
    <p>{{ article.created_at | date:"SHORT_DATE_FORMAT" }}</p>
    <p>{{ article.updated_at | date:"M, j, Y" }}</p>
    <a href="/articles/">[BACK]</a>
    <a href="/articles/{{ article.pk }}/delete/">[DELETE]</a>  <!-- 추가 -->
    <a href="/articles/{{ article.pk }}/edit/">[EDIT]</a>  <!-- 추가 -->

{% endblock %}
```





========== CRUD 실습 ==========



```markdown
# CRUD 실습

## 0. students 앱을 만들어주세요.

- `django_crud` 프로젝트에서 진행해주세요.



## 1. Student 모델을 만들어주세요.

- `name`: 이름의 최대 길이는 20입니다.
- `email`: 이메일의 최대 길이는 20입니다.
- `birthday`: `DateField`를 이용해서 생일날짜를 저장해주세요.
- `age`: `IntegerField` 이용해주세요.

- `str`:  Student 모델의 인스턴스를 출력했을 때 함수를 사용하여 학생의 이름을 출력할 수 있도록 해주세요.



## 2. Student 모델을 Admin 사이트에 등록해주세요.

- `StudentAdmin` 클래스를 만들어주세요.
- `list_display` 이용하여 `Student` 모델의 필드값들을 관리자 페이지에서 볼 수 있도록 설정해주세요.



## 3. 전체 학생 목록을 보여주는 페이지를 구성해주세요.

- 경로는 `/students/` 입니다.
```





















========== url 태그 ==========

만약 html파일에다 링크를 하드코딩 했다면, 나중에 사이트 주소가 바뀌었을 때 일일이 손으로 수정해줘야 한다.

하지만, 페이지 수가 많고 찾기가 힘들 수 있습니다. 따라서 url 태그를 사용해야 한다.



`django_crud` > `articles` > `urls.py`

```python
from django.urls import path
from . import views

app_name = 'articles'    # 앱 이름 설정 - 이걸 해야 편하다

urlpatterns = [
    path('', views.index, name="index"),
    path('new/', views.new, name="new"),
    path('create/', views.create, name="create"),
    path('detail/<int:pk>/', views.detail, name="detail"),
    path('<int:pk>/delete/', views.delete, name="delete"),
    path('<int:pk>/edit/', views.edit, name="edit"),
    path('<int:pk>/update/', views.update, name="update")
]
```

```
# 앱 이름을 설정하면 html 파일에서 <a href="{% url 'articles:edit' article.pk %}">
# 위와 같이 사용해야 하고, 만약 앱 이름이 없다면,
# <a href="{% url 'edit' article.pk %}">과 같이 사용합니다.
```





`django_crud` > `articles` > `templates` > `articles` > `detail.html` 

```html
<!-- templates/articles/detail.html -->

{% extends 'base.html' %}

{% block content %}

    <h1 class="text-center">DETAIL</h1>
    <h2>{{ article.pk }}번째 글</h2>
    <hr>
    <p>{{ article.title }}</p>
    <p>{{ article.content }}</p>
    <p>{{ article.created_at | date:"SHORT_DATE_FORMAT" }}</p>
    <p>{{ article.updated_at | date:"M, j, Y" }}</p>
    <a href="{% url 'articles:index' %}">[BACK]</a>
    <a href="{% url 'articles:delete' article.pk %}" onclick="return confirm('삭제하시겠어요?')">[DELETE]</a>
    <a href="{% url 'articles:edit' article.pk %}">[EDIT]</a>

{% endblock %}
```



`django_crud` > `articles` > `views.py`

```python
def func1(request):
    # 아래와 같이 사용할 수 있다.
    return redirect('articles:index')
```











========== HTTP 기초 ==========























========== RESTful하게 앱 바꾸기 ==========



`django_crud` > `articles` > `urls.py`

```python
from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    # # 기존 url
    # path('', views.index, name="index"),
    # path('new/', views.new, name="new"),
    # path('create/', views.create, name="create"),
    # path('detail/<int:pk>/', views.detail, name="detail"),
    # path('<int:pk>/delete/', views.delete, name="delete"),
    # path('<int:pk>/edit/', views.edit, name="edit"),
    # path('<int:pk>/update/', views.update, name="update")

    # 변경 후 url
    path('', views.index, name="index"),
    path('create/', views.create, name="create"),
    path('<int:pk>/', views.detail, name="detail"),
    path('<int:pk>/delete/', views.delete, name="delete"),
    path('<int:pk>/update/', views.update, name="update")
]
```



`django_crud` > `articles` > `views.py`

new 메소드를 삭제해 주고 create와 합쳐준다.

```python
def create(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        article = Article.objects.create(title=title, content=content)
        return redirect('articles:detail', article.pk)
    else:
        return render(request, 'articles/new.html')
```



`django_crud` > `articles` > `views.py`

edit 메소드를 삭제해주고 update와 합쳐준다.

```python
def update(request, pk):
    article = Article.objects.get(pk=pk)
    if request.method =="POST":
        title = request.POST.get('title')
        content = request.POST.get('content')

        article.title = title
        article.content = content

        article.save()

        return redirect('articles:index')
    else:
        context = {
            'article': article
        }
        return render(request, 'articles/update.html', context)
```



`django_crud` > `articles` > `templates` > `articles` > `edit.html` 을 `update.html`로 파일명을 바꾼 후 코드도 아래와 같이 수정한다.

```html
<!-- templates/articles/update.html -->

{% extends 'base.html' %}

{% block content %}

    <h1 class="text-center">UPDATE</h1>
    <form action="{% url 'articles:update' article.pk %}" method="POST">
        {% csrf_token %}
        <input type="text" name="title" value="{{ article.title }}"><br>
        <textarea name="content" id="" cols="30" rows="10">{{ article.content }}</textarea><br>
        <input type="submit" value="submit">
    </form>

{% endblock %}
```



`django_crud` > `articles` > `templates` > `articles` > `detail.html` 

```html
<!-- templates/articles/detail.html -->

{% extends 'base.html' %}

{% block content %}

    <h1 class="text-center">DETAIL</h1>
    <h2>{{ article.pk }}번째 글</h2>
    <hr>
    <p>{{ article.title }}</p>
    <p>{{ article.content }}</p>
    <p>{{ article.created_at | date:"SHORT_DATE_FORMAT" }}</p>
    <p>{{ article.updated_at | date:"M, j, Y" }}</p>
    <a href="{% url 'articles:index' %}">[BACK]</a>
    <a href="{% url 'articles:delete' article.pk %}" onclick="return confirm('삭제하시겠어요?')">[DELETE]</a>
    <a href="{% url 'articles:update' article.pk %}">[Update]</a>

{% endblock %}
```







========== 절대경로로 바꿔주는 기능 ==========



`django_crud` > `articles` > `models.py`

```python
from django.urls import reverse

class Article(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):    # 이거 추가
        # ex) 'articles/10/'
        return reverse('articles:detail', args=[str(self.pk)])
```



 index.html파일에서는 주석처리된 부분과 같은 기능을 아래의 a태그에서 가능하도록 해줍니다. 

`django_crud` > `articles` > `templates` > `articles` > `index.html` 

```html
<!-- templates/articles/index.html -->

{% extends 'base.html' %}

{% block content %}
    <h1 class="text-center">Articles</h1>
    <ul>
        {% for article in articles %}
            <p>글 번호: {{ article.pk }}</p>
            <p>글 제목: {{ article.title }}</p>
            <p>글 내용: {{ article.content }}</p>
            <!-- <a href="{% url 'articles:detail' article.pk %}">[DETAIL]</a> -->
            <a href="{{ article.get_absolute_url }}">[DETAIL]</a>
            <hr>
        {% endfor %}
    </ul>
{% endblock %}
```



 views.py에서도 아래와 같이 redirect를 간단하게 사용할 수 있습니다. 

`django_crud` > `articles` > `views.py`

```python
def delete(request, pk):
    article = Article.objects.get(pk=pk)
    if request.method == "POST":
        article.delete()
        return redirect('articles:index')
    else:
        # return redirect('articles:detail', article.pk)  # before
        return redirect(article)  # after
```



위에서 delete 메소드를 POST로부터 받을때만 작동되게 했으므로 detail.html 페이지에서 [DELETE] 버튼도 바꿔준다.

`django_crud` > `articles` > `templates` > `articles` > `detail.html` 

```html
...
<!-- <a href="{% url 'articles:delete' article.pk %}" onclick="return confirm('삭제하시겠어요?')">[DELETE]</a> -->
<form action="{% url 'articles:delete' article.pk %}" method="POST">
    {% csrf_token %}
    <input type="submit" value="DELETE" onclick="return confirm('삭제하시겠어요?')">
</form>
...
```





































































































