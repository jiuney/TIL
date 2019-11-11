# 회원가입 페이지 만들기



## 0. 프로젝트 가져오기

이전 프로젝트에서 이어서 할건데 내가 수업에 안왔어서;; 강사님 git에서 기존 프로젝트를 가져온다.

```bash
python -m venv venv
activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

* venv는 git에 없으므로 복사가 안되니까 복사한 폴더 내에 venv 폴더 만들고 가상환경 활성화를 먼저 해준다.
* model migration이랑 관리자 계정 만들기는 따로 해줘야 한다.



## 1. 앱 만들기

`accounts` 라는 앱을 만든다.

```bash
python manage.py startapp accounts
```

프로젝트 폴더인 `myform` 폴더 내의 `settings.py` 수정.

```python
INSTALLED_APPS = [
    'accounts',
    ...
]
```

`myform` > `urls.py` 수정.

```python
urlpatterns = [
    ...
    path('accounts/', include('accounts.urls')),
]
```



## 2. 회원가입 페이지 만들기

`accounts` > `urls.py` 생성.

```python
from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('signup/', views.signup, name="signup"),
]
```

`accounts` > `views.py` 에 signup 메소드 추가.

```python
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def signup(request):
    if request.method == "POST":
        pass
    else:
        form = UserCreationForm()
    context = {'form': form}
    return render(request, 'accounts/signup.html', context)
```

`accounts` > `templates` 폴더 생성 > `accounts` 폴더 생성 > `signup.html` 생성.

```html
{% extends 'base.html' %}
{% load bootstrap4 %}

{% block body %}

<h1>회원 가입</h1>
<form action="" method="POST">
    {% csrf_token %}
    {% bootstrap_form form %}
    {% buttons submit="회원 가입" reset="Cancel" %}{% endbuttons %}
</form>

{% endblock %}
```

`accounts` > `views.py` 수정.

```python
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('articles:index')
    else:
        form = UserCreationForm()
    context = {'form': form}
    return render(request, 'accounts/signup.html', context)
```



# 로그인 페이지 만들기

`accounts` > `views.py` 에 login 메소드 생성.

```python
...
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

...

def login(request):
    if request.method == "POST":
        pass
    else:
        form = AuthenticationForm()
    context = {'form': form}
    return render(request, 'accounts/login.html', context)
```

`accounts` > `templates` > `accounts` > `login.html` 생성.

```html
{% extends 'base.html' %}
{% load bootstrap4 %}

{% block body %}

<h1>로그인</h1>
<form action="" method="POST">
    {% csrf_token %}
    {% bootstrap_form form %}
    {% buttons submit="로그인" reset="Cancel" %}{% endbuttons %}
</form>

{% endblock %}
```

`accounts` > `urls.py` 수정.

```python
urlpatterns = [
    ...
    path('login/', views.login, name="login"),
]
```

`accounts` > `views.py` 에 login 메소드 수정.

```python
...
from django.contrib.auth import login as auth_login

...

def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('articles:index')
    else:
        form = AuthenticationForm()
    context = {'form': form}
    return render(request, 'accounts/login.html', context)
```

* `django.contrib.auth` 에서 `login`을 import 할 때 `auth_login` 이라는 이름으로 import하는 이유는 우리가 직접 만드는 login 메소드와 헷갈리지 않기 위해서이다.

로그인 후에는 목록 페이지에서 로그인한 사용자의 정보(아이디)가 보이게끔 `myform` > `templates` > `base.html` 수정.

```html
...
<body>
    <div class="container">
        <h3>Hello, {{ user.username }}</h3>
        <hr>
        {% block body %}
        {% endblock %}
    </div>
    {% bootstrap_javascript jquery="full" %}
</body>
</html>
```

* 여기서는 user를 안보내줘도 {{ user.username }}으로 불러올 수 있다 (request에 들어있어서).



# 로그아웃 페이지 만들기

`accounts` > `views.py` 에 logout 메소드 생성.

```python
...
from django.contrib.auth import logout as auth_logout

...

def logout(request):
    auth_logout(request)
    return redirect('articles:index')
```

* `logout`도 마찬가지로 `auth_logout`이라는 이름으로 import해서 우리가 만드는 logout 메소드와 헷갈리지 않도록 한다.

`accounts` > `urls.py` 수정.

```python
urlpatterns = [
    ...
    path('logout/', views.logout, name="logout"),
]
```

`myform` > `templates` > `base.html` 수정.

```html
...
<body>
    <div class="container">
        <h3>
            Hello, {{ user.username }}
            <a href="{% url 'accounts:logout' %}">로그아웃</a>
        </h3>
        <hr>
        {% block body %}
        {% endblock %}
    </div>
    {% bootstrap_javascript jquery="full" %}
</body>
</html>
```

그런데 이 경우 로그아웃해도 로그아웃 버튼이 안사라진다.

따라서 아래와 같이 수정한다.

`myform` > `templates` > `base.html`

```html
...
<body>
    <div class="container">
        {% if user.is_authenticated %}
            <h3>
                Hello, {{ user.username }}
                <a href="{% url 'accounts:logout' %}">로그아웃</a>
            </h3>
        {% else %}
            <h3>
                <a href="{% url 'accounts:login' %}">로그인</a>
                <a href="{% url 'accounts:signup' %}">회원가입</a>
            </h3>
        {% endif %}
        <hr>
        {% block body %}
        {% endblock %}
    </div>
    {% bootstrap_javascript jquery="full" %}
</body>
</html>
```



# 로그인 한 상태일 때



## 1. 로그인 된 상태에서 또 로그인 페이지에 들어가지는 현상 막기

`accounts` > `views.py` 수정.

```python
...

def signup(request):

    if request.user.is_authenticated:
        return redirect('articles:index')
    
    ...

def login(request):

    if request.user.is_authenticated:
        return redirect('articles:index')

    ...

...
```

* 이렇게 하면 로그인 한 상태에서 로그인 페이지나 회원가입 페이지로 접근했을 때 그냥 인덱스 페이지로 연결된다.



## 2. 회원가입하면 바로 로그인되도록 하기

`accounts` > `views.py` 수정.

```python
...

def signup(request):

    ...
    
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('articles:index')
    
    ...

...
```

* form을 통해 회원가입 정보를 만들 때 그 정보를 바로 user에 저장해서 로그인 메소드에 보내는 것.



## 3. 로그인 했을 경우에만 글쓰기/수정/삭제 가능하게 하기

`articles` > `templates` > `articles` > `index.html` 수정해서 로그인 했을 때에만 글쓰기 버튼이 보이도록 하기.

```html
{% extends 'base.html' %}

{% block body %}
    <h1>Articles</h1>
    {% if user.is_authenticated %}
        <a href="{% url 'articles:create' %}">[NEW]</a>
    ...
{% endblock %}
```

`articles` > `views.py` 수정해서 글쓰기/삭제/수정 페이지로 바로 접근하는 것 막기.

```python
...
from django.contrib.auth.decorators import login_required

...

# 이런 식으로도 사용 가능하다! @login_required(login_url="/accounts/test/")
@login_required
def create(request):
    ...

@login_required
@require_POST
def delete(request, article_pk):
    ...

@login_required
def update(request, article_pk):
    ...

...
```



## 4. 로그인 후 바로 메소드 실행되도록 하기

`accounts` > `views.py` 수정.

```python
def login(request):

    ...

    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'articles:index')
    
    ...
```

* decorator로 `@login_requred` 를 붙이게 되면, 주소를 통해 그 메소드로 바로 접근하려고 할 때 로그인 페이지로 이동되면서 동시에 쿼리로 next가 생성되면서 내가 원래 접근하려던 페이지가 들어가게 된다.
  * 예를 들어, 로그인을 안한 상태에서 `http://localhost:8000/articles/create/` 로 바로 접근하려고 하면 `http://localhost:8000/accounts/login/?next=/articles/create/` 로 연결되어서, next 쿼리가 생긴다.
* 그래서 위 코드처럼 `request.GET.get('next')` 를 써주게 되면 로그인 후 내가 원래 접근하려던 페이지로 이동된다. 만약 그렇지 않을 경우 or을 통해 index로 이동시켜준다.



















