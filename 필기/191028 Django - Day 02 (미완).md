# Django 설치 복습

1. 프로젝트를 넣을 폴더 생성

2. 생성된 폴더 안에서 vscode 실행 후 bash terminal에서 가상환경 설치

   ```bash
   python -m venv venv
   ```

3. 가상환경 활성화

   ```bash
   activate
   ```

   * 이전 필기에 activate 설정해둔거 참고

4. django 프로젝트 만들기

   ```bash
   django-admin startproject django_intro_recap .
   ```

   * 꼭 외워두기!
   * `django_intro_recap`이라는 이름의 프로젝트를 만든 것.

5. django 서버 실행

   ```bash
   python manage.py runserver
   ```

   * 꼭 외워두기!

6. bash를 계속 써야하니까 일단 서버 끄기

   ```bash
   ctrl+C
   ```

7. `pages`라는 이름의 앱 만들기

   ```bash
   python manage.py startapp pages
   ```

8. `django_intro_recap`폴더 안의 `settings.py`에 설치한 앱 지정해주기

   ```python
   INSTALLED_APPS = [
       'pages', # 이렇게 새 앱 추가
       'django.contrib.admin',
       'django.contrib.auth',
       'django.contrib.contenttypes',
       'django.contrib.sessions',
       'django.contrib.messages',
       'django.contrib.staticfiles',
   ]
   ```

9. `pages`폴더 안에 `templates`폴더를 만들고 그 안에 또 `pages`폴더를 만든다

   * 앞으로 html 파일들을 `templates` 안에 있는 `pages`폴더에 넣을 것
   * 왜 이렇게 만드는지는 이전 필기 참고

10. 이후에는 `django_intro_recap`폴더 안의 `urls.py`, `pages`폴더 안의 `views.py`, `templates`폴더 안의 `pages`폴더 안에 html 파일들을 설정해가면 된다.



## 첫 페이지 설정

1. `urls.py`에서 주소 추가

   ```python
   from pages import views
   
   urlpatterns = [
       path('admin/', admin.site.urls),
       path('', views.index)
   ]
   ```

2. `views.py`에서 index함수 추가

   ```python
   def index(request):
       return render(request, 'pages/index.html')
   ```

3. `templates`폴더 안의 `pages`폴더 안에 `index.html`추가

4. `index.html`수정

5. 인터넷창에서 `localhost:8000` 입력해서 페이지 확인



## throw&catch 연습

1. `views.py`에서 throw와 catch 함수 추가

   ```python
   def throw(request):
       return render(request, 'pages/throw.html')
   
   def catch(request):
       message = request.GET.get("message")
       message2 = request.GET.get("message2")
       context = {
           'message': message,
           'message2': message2
       }
       return render(request, 'pages/catch.html', context)
   ```

2. `urls.py`에서 주소 추가

   ```python
   urlpatterns = [
       path('admin/', admin.site.urls),
       path('', views.index),
       path('throw/', views.throw),
       path('catch/', views.catch),
   ]
   ```

3. `templates`폴더 안의 `pages`폴더 안에 `throw.html` 만들고 설정

   ```html
   <form action="/catch/" method="GET">
       <input type="text" name="message">
       <input type="text" name="message2">
       <input type="submit">
   </form>
   ```

4. `templates`폴더 안의 `pages`폴더 안에 `catch.html` 만들고 설정

   ```html
   <h1>
       네가 던져서 내가 받은건 <br>
       "{{ message }}"랑<br>
       "{{ message2 }}"야!
   </h1>
   ```

5. 인터넷창에서 `localhost:8000/throw` 입력해서 페이지 확인

6. 위 페이지에서 각각 메세지 입력 후 제출 눌러서 `catch`페이지 확인



## 로또 당첨 번호 가져오기

1. django 서버 끄고 `requests` 설치

   ```bash
   pip install requests
   ```

2. `views.py`에 `requests` import

   ```python
   import requests
   ```

3. 













form tag에서 GET으로 보낸 정보는 주소창에 ? 뒤에 쿼리스트링으로 나타난다

POST는 {% csrf_token %}