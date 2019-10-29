# Database



## 기본 용어

* scheme (스키마): 데이터베이스에서 자료의 구조, 표현 방법, 관계 등을 정의한 구조.
* table: 행과 열로 데이터의 관계를 표현.
* column: 각 열에는 고유한 데이터 형식이 지정된다.
* row: 테이블의 데이터는 행에 저장된다. 각 줄을 record라고 한다.
* PK (기본키): 각 행(레코드)의 고유값으로 Primary Key라고 불린다.



## SQL

* SQL (Structured Query Language)
  * 3종류로 구분
    * DDL (데이터 정의 언어)
    * DML (데이터 조작 언어)
    * DCL (데이터 제어 언어)

* SQL Keywords
  * INSERT
  * DELETE
  * SELECT
  * UPDATE

* CRUD (Create, Read, Update, Delete)
    | CRUD   | SQL    |
    | ------ | ------ |
    | Create | INSERT |
    | Read   | SELECT |
    | Update | UPDATE |
    | Delete | DELETE |



# SQLite 설치

1. [홈페이지](https://www.sqlite.org/download.html)에서 Precompiled Binaries for Windows에서 자신의 컴퓨터에 맞는 버전 다운로드.

2. 압축 풀고 C폴더 밑에 폴더 채 넣고 폴더이름 `sqlite`로 바꾸기.

3. 윈도우 검색으로 `시스템 환경 변수 편집` 검색해서 들어가기.

4. `환경 변수` 클릭해서 `사용자 변수`에서 `Path` 더블클릭해서 들어가기.

5. `새로 만들기` 클릭해서 `C:\sqlite` 넣고 확인.

6. (아무데서나) bash 열고 vim 편집기 열기.

   ```bash
   vim ~/.bashrc
   ```

7. vim 편집기에서 `i` 눌러서 편집모드로 들어간 후 다음 구문 넣기.

   ```bash
   alias sqlite3="winpty sqlite3"
   ```

8. 위의 구문을 다 쓰고 나면 `esc` 눌러서 편집모드를 나온 후에 `:wq`를 입력하고 엔터쳐서 저장.

9. bash에서 `sqlite3`을 쳤을 때 버전 정보가 나오면 성공.



# Django에서 Model 설정

1. `django_orm` 폴더 생성

   ```bash
   mkdir django_orm
   cd django_orm    # django_orm 폴더로 이동
   ```

2. `django_orm`폴더 내에 가상환경 생성하고 활성화 및 django 설치

   ```bash
   python -m venv venv
   activate
   pip install django
   ```

3. django project `crud` 생성

   ```bash
   django-admin startproject crud .
   ```

4. django app `articles` 생성

   ```bash
   python manage.py startapp articles
   ```

5. `crud`폴더 내의 `settings.py` 변경

   ```python
   INSTALLED_APPS = [
       'articles',    # 이 줄 추가
       'django.contrib.admin',
       'django.contrib.auth',
       'django.contrib.contenttypes',
       'django.contrib.sessions',
       'django.contrib.messages',
       'django.contrib.staticfiles',
   ]
   ```

6. `articles` 앱 내의 `models.py` 설정

   ```python
   # Create your models here.
   
   class Article(models.Model):
       title = models.CharField(max_length=50)
       content = models.TextField()
       created_at = models.DateTimeField(auto_now_add=True)
       updated_at = models.DateTimeField(auto_now=True)
   ```

   * CharField는 길이 제한 있다 > 반드시 max_length 지정
   * TextField는 길이 제한 없음

7. migration 파일 생성

   ```bash
   python manage.py makemigrations
   ```

   * 어떻게 변경할 건지 설계도를 만든 것

8. 변경 적용

   ```bash
   python manage.py migrate
   ```

   * migrations 파일을 토대로 변경을 적용

9. DB 확인

   ```bash
   sqlite3 db.sqlite3
   ```

   * 이렇게 하면 sqlite를 조작할 수 있게 된다

   * 이 상태에서 

     ```shell
     .tables
     ```

     * 이 구문을 치면 DB내의 table들 목록을 보여준다
     * 아까 만든 `articles_article`이 생성되어 있음을 확인한다.

   * sqlite에서 빠져나온다

     ```shell
     .exit
     ```

10. 참고: bash를 통해 SQL문을 자동으로 만들어 줄 수도 있다

    ```bash
    python manage.py sqlmigrate articles 0001
    ```

    * 이걸 치면 SQL문이 프린트된다. 내가 만든 모델을 SQL문으로 생성하려면 어떻게 쓰면 되는지를 알려주는 것으로, 번역만 해줄 뿐이지 뭔가 변화를 일으키지는 않는다.

11. migration 확인

    ```bash
    python manage.py showmigrations
    ```

    * 변경된 내용 확인



## 요약

1. models.py: 모델 작성 및 변경
2. makemigrations: migration 파일 생성 (설계도)
3. migrate: 실제 DB에 적용 (테이블 생성)



# 데이터 입력 (Create)

0. bash에서 sqlite를 조작할 수 있는 shell로 들어간다

   ```bash
   python manage.py shell
   ```

1. 설정한 모델인 `Article`을 불러온다

   ```shell
   from articles.models import Article
   ```

2. `Article`에 뭐가 있나 확인

   ```shell
   Article.objects.all()
   ```

   * queryset은 반환되는 객체의 집합
   * queryset은 리스트처럼 다룰 수 있다

3. `Article`에 첫번째 데이터인 `article1` 생성

   ```shell
   article1 = Article()
   ```

   * 이렇게 나오면 제대로 생성된 것

     ```shell
     >>> article1
     <Article: Article object (None)>
     ```

4. `article1`에 내용을 넣는다

   * 제목을 넣는다

     ```shell
     article1.title = '1번 제목'
     ```

   * 내용을 넣는다

     ```shell
     article1.content = '1번 내용'
     ```

5. 입력한 데이터 확인

   * 제목 확인

     ```shell
     >>> article1.title
     '1번 제목'
     ```

   * 내용 확인

     ```shell
     >>> article1.content
     '1번 내용'
     ```

6. 입력한 내용을 저장한다

   ```shell
   article1.save()
   ```

   * save 메소드가 호출되기 전까지는 DB에 반영이 안된다.

   * `article1`을 확인했을 때 이렇게 출력되면 제대로 저장된 것

     ```shell
     >>> article1
     <Article: Article object (1)>
     ```

7. 데이터가 입력된 시간 확인

   ```shell
   >>> article1.created_at
   datetime.datetime(2019, 10, 29, 1, 49, 25, 616275, tzinfo=<UTC>)
   ```

8. 데이터를 바로 입력하는 방식으로 두번째 레코드를 생성한다

   ```shell
   article2 = Article(title = '2번 제목', content = '2번 내용')
   ```

9. `article2`를 저장한다 (저장까지 해줘야 한다)

   ```shell
   article2.save()
   ```

10. 잘 저장되었는지 확인

    ```shell
    >>> article2
    <Article: Article object (2)>
    ```

11. 레코드를 입력과 동시에 바로 저장할 수도 있다

    ```shell
    Article.objects.create(title = '3번 제목',  content = '3번 내용')
    ```

    * 이렇게 하면 save할 필요 없이 바로 저장되어 다음과 같이 출력된다

      ```shell
      >>> Article.objects.create(title = '3번 제목',  content = '3번 내용')
      <Article: Article object (3)>
      ```



# 데이터 읽기 (Read)

* 새 레코드 생성

  ```shell
  article4 = Article()
  article4.title = '4번 제목'
  ```

  * title만 있고 content는 없는 레코드가 생성된다.

* 유효성 검사

  ```shell
  article4.full_clean()
  ```

  * article4를 데이터베이스에 저장해도 되는지 유효성검사 해주는 구문

  * 빈 열이 있으면 validation error가 나온다

  * 근데 빈칸이 있어도 저장은 된다

    ```shell
    article4.save()
    ```

* 데이터 전체 확인하기

  ```shell
  Article.objects.all()
  ```



## 출력 내용 표현 방법 바꾸기

1. `django_orm` 폴더 내의 `articles` 폴더 내의 `models.py`에 다음 구문 추가

   ```python
   # Create your models here.
   
   class Article(models.Model):
       title = models.CharField(max_length=50)
       content = models.TextField()
       created_at = models.DateTimeField(auto_now_add=True)
       updated_at = models.DateTimeField(auto_now=True)
   
       def __str__(self):    # 이 함수 추가
           return f'{self.id}번글 - {self.title} : {self.content}'
   ```

2. shell에서 모델 다시 불러오기

   ```shell
   from articles.models import Article
   ```

3. 데이터 다시 확인해서 출력 내용이 바뀌었나 확인하기

   ```shell
   Article.objects.all()
   ```

   * 출력 내용이 내가 설정한 대로 이렇게 나온다

     ```shell
     >>> Article.objects.all()
     <QuerySet [<Article: 1번글 - 1번 제목 : 1번 내용>, <Article: 2번글 - 2번 제목 : 2번 내용>, <Article: 3
     번글 - 3번 제목 : 3번 내용>, <Article: 4번글 - 4번 제목 : >]>
     ```

   * 안바뀌었다면 shell 다시 켜기



## 조건문 (where)

* get으로 가져오기

  ```shell
  article3 = Article.objects.get(pk=3)
  article3
  ```

* filter로 가져오기

  ```shell
  article = Article.objects.filter(title = '3번 제목')
  article3
  ```

* 마지막 레코드 가져오기

  ```shell
  article = Article.objects.all().last()
  article
  ```



### get과 filter 비교

* get

  ```shell
  article = Article.objects.get(pk=1)
  type(article)
  ```

  * get이 반환하는 값 = 인스턴스

* filter

  ```shell
  article = Article.objects.filter(pk=1)
  type(article)
  ```

  * filter가 반환하는 값 = 쿼리 셋

* 없는 레코드 불러올 때

  * get

    ```shell
    article = Article.objects.get(pk=10)
    article
    ```

    * 에러

  * filter

    ```shell
    article = Article.objects.filter(pk=10)
    article
    ```

    * 빈 쿼리 셋



## 출력 순서

* order_by

  ```shell
  articles = Article.objects.all().order_by('pk')
  articles
  ```

  * pk 기준으로 정렬

  * 기본값이 오름차순

  * 내림차순은 다음과 같다

    ```shell
    articles = Article.objects.all().order_by('-pk')
    articles
    ```



## 쿼리셋

쿼리셋은 리스트처럼 다룰 수 있다

* 인덱싱

  ```shell
  articles = Article.objects.all()[0]
  articles
  ```

* 슬라이싱

  ```shell
  articles = Article.objects.all()[:2]
  articles
  ```



## 유사한 내용 찾기

* contains

  ```shell
  articles = Article.objects.filter(title__contains='1번')
  articles
  ```

  * 제목에 "1번"이라는 내용이 포함되어있는 레코드 가져오기

* startswith

  ```shell
  articles = Article.objects.filter(title__startswith='1')
  articles
  ```

  * 제목이 "1"로 시작하는 레코드 가져오기

* endswith

  ```shell
  articles = Article.objects.filter(title__endswith='목')
  articles
  ```

  * 제목이 "목"으로 끝나는 레코드 가져오기



# 데이터 업데이트 (Update)

```shell
article = Article.objects.get(pk=1)
article.title = '1번 제목 (2)'
article.save()
Article.objects.all()
```

* pk가 1인 레코드의 title을 위와 같이 바꿔준다
* 위의 코드처럼 수정 내용을 변수에 담아준 후 저장하는 방식으로 업데이트 한다



# 데이터 삭제 (Delete)

```shell
article1 = Article.objects.get(pk=1)
article1.delete()
Article.objects.all()
```

* 업데이트와 마찬가지로 제거하려는 레코드를 가져와 변수에 담아준 후 삭제한다



# 참고

* shell에서 나올 땐 `exit()`



# 관리자 페이지

* 관리자 페이지 접속

  * 서버를 켜고

    ```bash
    python manage.py runserver
    ```

  * [localhost:8000/admin](localhost:8000/admin) 에 접속

  * 로그인 페이지가 나온다

* 관리자 계정 만들기

  * 서버를 끄고 (`ctrl+C`)

  * 관리자 계정인 `superuser`를 만든다

    ```bash
    python manage.py createsuperuser
    ```

  * user: admin
    이메일 주소: admin@hotmail.com
    Password: Qwer1234



## 웹 관리 페이지에서 모델 조작하기

* 모델 보이게 하기

* `django_orm` 폴더 밑에 `articles` 폴더 밑에 `admin.py` 수정

  ```python
  from django.contrib import admin
  from .models import Article
  
  # Register your models here.
  
  admin.site.register(Article, ArticleAdmin)
  ```

* 웹 관리 페이지에서 보이는 데이터 목록 출력 내용 변경

  ```python
  from django.contrib import admin
  from .models import Article
  
  # Register your models here.
  
  class ArticleAdmin(admin.ModelAdmin):
      list_display = ('pk', 'title', 'content', 'created_at', 'updated_at')
  
  admin.site.register(Article, ArticleAdmin)
  ```

* 웹 관리 페이지에서 보이는 데이터 목록 옆에 필터 생성

  ```python
  from django.contrib import admin
  from .models import Article
  
  # Register your models here.
  
  class ArticleAdmin(admin.ModelAdmin):
      list_display = ('pk', 'title', 'content', 'created_at', 'updated_at')
      list_filter = ('created_at',)
  
  admin.site.register(Article, ArticleAdmin)
  ```

  * list_filter는 튜플 형식이어야 하기 때문에 `'created_at'` 다음에 `,`를 찍어준다



# django-extensions의 shell_plus

* django의 extension중 하나인 shell_plus로 더 편한 shell을 쓸 수 있다 (model을 알아서 불러와주는 등)



## 설치 방법

1. bash에서 django-extensions 설치

   ```bash
   pip install django-extensions
   ```

2. `django_orm` 폴더 밑의 프로젝트 폴더인 `crud` 폴더 안에 있는 `settings.py` 에 django-extensions를 추가

   ```python
   INSTALLED_APPS = [
       'articles',
       'django.contrib.admin',
       'django.contrib.auth',
       'django.contrib.contenttypes',
       'django.contrib.sessions',
       'django.contrib.messages',
       'django.contrib.staticfiles',
       'django_extensions',    # 추가
   ]
   ```

3. shell_plus 실행

   ```bash
   python manage.py shell_plus
   ```

   

# 레코드를 입력하는 세가지 방법

(shell_plus에서 계속)

1. 첫번째 방법: 차근차근 하나하나 입력

   ```shell
   article = Article()
   article.title = '1번 제목'
   article.content = '1번 내용'
   article.save()
   ```

2. 두번째 방법: 인스턴스 생성과 동시에 키워드로 값 넣어주기

   ```shell
   article2 = Article(title = '2번 제목 2', content = '2번 내용 2')
   article2.save()
   ```

3. 세번째 방법: create method

   ```shell
   Article.objects.create(title = '3번 제목 2', content = '3번 내용 2')
   Article.objects.all()
   ```



# 복습 및 응용: 웹페이지까지 만들어보기



## 복습: 프로젝트와 앱 만들고 모델까지 만들기

1. 새 폴더 `django_crud` 만들기

   ```bash
   mkdir django_crud
   cd django_crud
   ```

2. 가상환경 만들고 활성화

   ```bash
   python -m venv venv
   activate
   ```

3. django 설치

   ```bash
   pip install django
   ```

4. `crud`라는 이름의 프로젝트 만들기

   ```bash
   django-admin startproject crud .
   ```

5. `articles`라는 이름의 앱 만들기

   ```bash
   python manage.py startapp articles
   ```

6. `django_crud` > `crud` > `settings.py`에 `articles` 추가

   ```python
   INSTALLED_APPS = [
       'articles',    # 추가
       'django.contrib.admin',
       'django.contrib.auth',
       'django.contrib.contenttypes',
       'django.contrib.sessions',
       'django.contrib.messages',
       'django.contrib.staticfiles',
   ]
   ```

7. `django_crud` 밑의 `crud`와 `articles` 폴더 및에 각각 `templates` 폴더 만들기

8. `django_crud` > `articles` > `templates` 밑에 `articles` 폴더 만들기

9. `django_crud` > `crud` > `settings.py` 수정

   ```python
   TEMPLATES = [
       {
           'BACKEND': 'django.template.backends.django.DjangoTemplates',
           'DIRS': [os.path.join(BASE_DIR, 'crud', 'templates')],  # 여기 수정
           'APP_DIRS': True,
           'OPTIONS': {
               'context_processors': [
                   'django.template.context_processors.debug',
                   'django.template.context_processors.request',
                   'django.contrib.auth.context_processors.auth',
                   'django.contrib.messages.context_processors.messages',
               ],
           },
       },
   ]
   ```

10. `django_crud` > `crud` > `templates` > `base.html` 생성

    ```html
    <!-- crud/templates/base.html -->
    
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="X-UA-Compatible" content="ie=edge">
        <title>Document</title>
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

11. `django_crud` > `crud` > `urls.py` 수정

    ```python
    from django.contrib import admin
    from django.urls import path, include    # 여기 include 추가
    
    urlpatterns = [
        path('admin/', admin.site.urls),
        path('articles/', include('articles.urls')),   # 여기 추가
    ]
    ```

12. `django_crud` > `articles` > `urls.py` 생성

    ```python
    from django.urls import path
    from . import views
    
    urlpatterns = [
        path('', views.index),
    ]
    ```

13. `django_crud` > `articles` > `views.py` 수정

    ```python
    # Create your views here.
    
    def index(request):
        return render(request, 'articles/index.html')
    ```

14. `django_crud` > `articles` > `templates` > `articles` > `index.html` 생성

    ```html
    <!-- templates/articles/index.html -->
    
    {% extends 'base.html' %}
    
    {% block content %}
        <h1 class="text-center">Articles</h1>
    {% endblock %}
    ```

15. 서버 실행해보기

    ```bash
    python manage.py runserver
    ```

16. `django_crud` > `articles` > `models.py` 수정

    ```python
    from django.db import models
    
    # Create your models here.
    
    class Article(models.Model):
        title = models.CharField(max_length=20)
        content = models.TextField()
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)
    
        def __str__(self):
            return self.title
    ```

17. `ctrl+C`로 서버 끄기

18. 수정한 model migrate하기

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

    * 중요!!! models.py에 뭔가를 수정할 경우 그때마다 다시 migrate 해줘야 한다!



## 새 게시물 작성 페이지 만들기

1. `django_crud` > `articles` > `views.py` 수정

   ```python
   def new(request):
       return render(request, 'articles/new.html')
   ```

2. `django_crud` > `articles` > `templates` > `articles` > `new.html` 생성

   ```html
   <!-- templates/articles/new.html -->
   
   {% extends 'base.html' %}
   {% block content %}
       <h1 class="text-center">NEW</h1>
       <form action="/articles/create/" method="GET">
           <input type="text" name="title"><br>
           <textarea name="content" id="" cols="30" rows="10"></textarea><br>
           <input type="submit" value="submit">
       </form>
   {% endblock %}
   ```

3. `django_crud` > `articles` > `views.py` 수정해서 create 함수 생성

   ```python
   from .models import Article
   
   def create(request):
       title = request.GET.get("title")
       content = request.GET.get("content")
       Article.objects.create(title=title, content=content)
       return render(request, 'articles/create.html')
   ```

4. `django_crud` > `articles` > `templates` > `articles` > `create.html` 생성

   ```html
   <!-- templates/articles/create.html -->
   
   {% extends 'base.html' %}
   
   {% block content %}
       <h1 class="text-center">성공적으로 글이 작성되었습니다!</h1>
   {% endblock %}
   ```

5. `django_crud` > `articles` > `urls.py` 수정해서 url 생성

   ```python
   urlpatterns = [
       path('', views.index),
       path('new/', views.new),
       path('create/', views.create)
   ]
   ```

6. 서버 켜서 페이지 확인

   ```bash
   python manage.py runserver
   ```

   * 서버 끄기: `ctrl+c`



## 관리자 설정

* 관리자 페이지 설정: `django_crud` > `articles` > `admin.py` 수정

  ```python
  from django.contrib import admin
  from .models import Article
  
  # Register your models here.
  
  class ArticleAdmin(admin.ModelAdmin):
      list_display = ('pk', 'title', 'content', 'created_at', 'updated_at')
  
  admin.site.register(Article, ArticleAdmin)
  ```

* 관리자 계정 만들기: bash에 다음 코드 입력

  ```bash
  python manage.py createsuperuser
  ```

  * username: juh
    email: email@hotmail.com
    password: Qwer1234

* 서버 실행

* [http://localhost:8000/admin](http://localhost:8000/admin) 페이지에서 로그인 해보기

* Articles 페이지에서 레코드 추가해보기



## 메인 페이지에서 게시물이 보이도록 하기

1. `django_crud` > `articles` > `views.py` 수정

   ```python
   def index(request):
       articles = Article.objects.all()
       context = {
           'articles': articles
       }
       return render(request, 'articles/index.html', context)
   ```

2. `django_crud` > `articles` > `templates` > `articles` > `index.html` 수정

   ```html
   {% extends 'base.html' %}
   
   {% block content %}
       <h1 class="text-center">Articles</h1>
       {% for article in articles %}
           <p>글 번호: {{ article.pk }}</p>
           <p>글 제목: {{ article.title }}</p>
           <p>글 내용: {{ article.content }}</p>
           <hr>
       {% endfor %}
   {% endblock %}
   ```

3. [http://localhost:8000/articles/](http://localhost:8000/articles/) 에서 확인



## GET 방식을 POST 방식으로 바꾸기

http://localhost:8000/articles/new/ 의 문제점: 제목과 내용이 주소창에 다 뜬다.

해결 방법은 GET을 POST로 바꾸는 것.

1. `django_crud` > `articles` > `templates` > `articles` > `new.html` 수정

   ```html
   <!-- templates/articles/new.html -->
   
   {% extends 'base.html' %}
   
   {% block content %}
       <h1 class="text-center">NEW</h1>
       <form action="/articles/create/" method="POST">
           {% csrf_token %}
           <input type="text" name="title"><br>
           <textarea name="content" id="" cols="30" rows="10"></textarea><br>
           <input type="submit" value="submit">
       </form>
   {% endblock %}
   ```

2. `django_crud` > `articles` > `views.py` 수정

   ```python
   def create(request):
       title = request.POST.get("title")
       content = request.POST.get("content")
       Article.objects.create(title=title, content=content)
       return render(request, 'articles/create.html')
   ```



## 새 게시물 작성 후 바로 메인 페이지로 연결되도록 하기

* `django_crud` > `articles` > `views.py` 수정

  ```python
  from django.shortcuts import render, redirect
  
  def create(request):
      title = request.POST.get("title")
      content = request.POST.get("content")
      Article.objects.create(title=title, content=content)
      return redirect('/articles/')
  ```

* [http://localhost:8000/articles/new/](http://localhost:8000/articles/new/) 에서 게시물 작성해보고 잘 표시되는지 확인하기