# django 기본

MTV



# django 기본 설치

1. 일단 폴더에 venv 만들기

   ```bash
   python -m venv venv
   activate    # 가상 환경 activate
   ```

2. django 설치

   ```bash
   pip install django
   ```

3. django 프로젝트 시작하기

   ```bash
   django-admin startproject django_intro .
   ```

   * `django_intro`라는 이름의 프로젝트를 시작한다는 것
   * 마지막에 한 칸 띄고 `.`을 붙이는 것은 해당 폴더 내에 바로 프로젝트를 만든다는 것. 이걸 안해주면 폴더가 하나 더 생긴다.

4. 서버 켜기

   ```bash
   python manage.py runserver
   ```

   * bash에서 서버를 끄고 빠져나가고 싶을 때는 `ctrl+c`

5. 앱 만들기

   * 회원관리, 게시판 등 기능에 따라 하나하나 앱을 만들어준다.

   ```bash
   python manage.py startapp pages
   ```

   * `pages`라는 이름의 앱을 생성.
   * 프로젝트 폴더의 settings.py에서 INSTALLED_APPS에 `'pages'` 추가

   ```python
   # Application definition
   
   INSTALLED_APPS = [
       'pages',
       'django.contrib.admin',
       'django.contrib.auth',
       'django.contrib.contenttypes',
       'django.contrib.sessions',
       'django.contrib.messages',
       'django.contrib.staticfiles',
   ]
   ```

   * 앱을 설정해도 django가 모르기 때문에 이렇게 알려준다.

6. 생성된 앱의 view 설정

   * pages 폴더 내의 views.py를 수정한다.

   ```python
   # Create your views here.
   def index(request):
       return render(request, 'index.html')
   ```

7. 프로젝트 폴더의 urls.py 수정

   * urls.py의 urlpatterns에 새 path 추가

     ```python
     urlpatterns = [
         path('admin/', admin.site.urls),
         path('index/', views.index)
     ]
     ```

     * django에서는 url 경로 마지막에 "/"를 붙여야 한다. (그냥 django의 특징이다)

8. index.html 생성

   * `pages `폴더 내에 `templates` 폴더 생성 후 그 안에 또 `pages` 폴더를 만든다.
     * html은 `templates` 폴더 안에 넣어주는 것이 상식(?)
     * 근데 앱 마다 다 `templates` 폴더가 만들어질 것이기 때문에 django가 구분하기 용이하게 `templates` 폴더 안에다가 앱 이름과 똑같은 폴더를 하나 더 생성해주는 것.
   * 원하는대로 html파일을 만든다

9. view 재수정

   * index.html파일의 위치를 제대로 적어준다.

   ```python
   # Create your views here.
   def index(request):
       return render(request, 'pages/index.html')
   ```

   * 경로에서 `templates`는 django가 알아서 잡아주기 때문에 `pages`부터 표기.













# 오늘 꼭 기억할 것

* django 프로젝트 만들기

  ```bash
  django-admin startproject django_intro .
  ```

* 서버 켜기

  ```bash
  python manage.py runserver
  ```