# 전생의 직업을 알려주는 앱 만들기

이전에 만들어 준 `crud` 프로젝트에 새 앱을 만들 것.

`django_crud` 폴더 내에서 vscode 열고 faker 설치.

```bash
activate
pip install faker
```

shell을 켜고 faker 사용법을 연습해볼 수 있다.

```bash
python manage.py shell
```

```shell
>>> from faker import Faker
>>> fake = Faker()
>>> fake.name()
'Harry Martinez'
>>> fake.address()
'97014 Danielle Ville\nSouth Kimberlyland, DE 80507'
>>> fake.job()
'Special educational needs teacher'
>>> fake = Faker('ko_KR')
>>> fake.name()
'황미영'
>>> fake.address()
'경상남도 과천시 역삼가'
>>> fake.job()
'방문 판매원'
>>> exit()
```

`jobs`라는 앱을 만든다.

```bash
python manage.py startapp jobs
```

`crud` 프로젝트에 `jobs` 앱이 설치되어 있음을 알려준다.

`django_crud` > `crud` > `setting.py`

```python
INSTALLED_APPS = [
    'jobs',    # 추가
    'articles',
    ...
]
```

`django_crud` > `jobs` > `models.py` 를 설정해준다.

```python
class Job(models.Model):
    name = models.CharField(max_length=20)
    past_job = models.TextField()

    def __str__(self):
        return self.name
```

수정된 model을 migrate 해준 후 서버를 켠다.

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

관리자 페이지에 `jobs` 앱 페이지를 만들어준다: `django_crud` > `jobs` > `admin.py`

```python
from django.contrib import admin
from .models import Job

# Register your models here.

class JobAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'past_job')

admin.site.register(Job, JobAdmin)
```

`django_crud` > `jobs` > `urls.py`  생성

```python
from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.index, name='index')
]
```

`django_crud` > `jobs` > `views.py` 에 index 메소드 생성.

```python
def index(request):
    return render(request, 'jobs/index.html')
```

`django_crud` > `jobs` > `templates` 생성 > `jobs` 생성 > `index.html` 생성.

```html
{% extends 'base.html' %}

{% block content %}

    <h1>전생의 직업</h1>
    <p>당신의 전생의 직업을 알려드립니다.</p>

    <form action="#" method="POST">
        {% csrf_token %}
        <label for="name">Name</label>
        <input type="text" name="name" id="name">
        <input type="submit" value="제출">
    </form>

{% endblock %}
```

`django_crud` > `crud` > `urls.py` 에 `jobs`앱에 대한 url 추가.

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('articles/', include('articles.urls')),
    path('jobs/', include('jobs.urls')),    # 추가
]
```

`django_crud` > `jobs` > `views.py` 에 past_life 메소드 생성.

```python
from .models import Job
from faker import Faker

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
        fake = Faker('ko_KR')
        fakejob = fake.job()
        Job.objects.create(name=name, past_job=fakejob)
    
    check = Job.objects.get(name=name)
    past_job = check.past_job

    context = {
        'name': name,
        'pastjob': past_job
    }

    return render(request, 'jobs/past_life.html', context)
```

`django_crud` > `jobs` > `templates` > `jobs` > `index.html` 에서 form action에 들어갈 링크 수정.

```html
<!-- templates/jobs/index.html -->

{% extends 'base.html' %}

{% block content %}

    <h1>전생의 직업</h1>
    <p>당신의 전생의 직업을 알려드립니다.</p>

    <form action="{% url 'jobs:past_life' %}" method="POST">
        {% csrf_token %}
        <label for="name">Name</label>
        <input type="text" name="name" id="name">
        <input type="submit" value="제출">
    </form>

{% endblock %}
```

`django_crud` > `jobs` > `urls.py` 에 past_life 링크 추가.

```python
urlpatterns = [
    path('', views.index, name='index'),
    path('past_life/', views.past_life, name='past_life'),
]
```

`django_crud` > `jobs` > `templates` > `jobs` > `past_life.html` 페이지 생성.

```html
<!-- templates/jobs/past_life.html --> -->

{% extends 'base.html' %}

{% block content %}

	<h1>{{ name }}님의 전생 직업은 "{{ pastjob }}" 입니다.</h1>

{% endblock%}
```



## 움짤 넣기 (준비)

서버끄고 bash에서 

```bash
pip install requests
```



### API KEY 숨기기

bash에서 python-decouple 설치.

```bash
pip install python-decouple
```

프로젝트 맨 바깥 폴더 (`django_crud`폴더 바로 밑, `crud`폴더와 같은 위치)에 `.env`파일 만들기

```bash
touch .env
```

.env 파일에 [GIPHY](https://developers.giphy.com/) 에서 가져온 API KEY 저장하기

```markdown
GIPHY_API_KEY=내api_key넣기
```



## 움짤 넣기

`django_crud` > `jobs` > `views.py` 에서 past_life 메소드 수정.

```python
import requests
from decouple import config

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
```

* 내가 쓴 코드대로 인덱스로 가져오면 KEY가 없을 경우 에러가 난다.
* 반면 강사님 코드대로 get으로 가져오면 KEY가 없을 경우에도 에러가 나지 않고 None값을 가져오게 된다.

`django_crud` > `jobs` > `templates` > `jobs` > `past_life.html` 을 이미지 파일이 출력되도록 수정한다.

```html
<!-- templates/jobs/past_life.html -->

{% extends 'base.html' %}

{% block content %}

    <h1>{{ name }}님의 전생 직업은 "{{ pastjob }}" 입니다.</h1>
    <img src="{{ gif_url }}}" alt="GIPHY_img_for_past_job">

{% endblock%}
```



# Articles 앱에 댓글 기능 만들기

## 댓글 만들기

게시물과 댓글에 필요한 요소는 다음과 같다.

| article                                                      | comment                                                      |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| PK (Primary Key)<br />title<br />content<br />created_at<br />updated_at | PK (Primary Key)<br />content<br />created_at<br />updated_at<br />FK (Foreign Key) |

* FK가 게시물 테이블과 댓글 테이블을 이어준다.
* 게시물 테이블과 댓글 테이블의 관계는 1:N (one-to-many).

`articles` 앱의 게시물들에 댓글을 만들려고 한다.

`django_crud` > `articles` > `models.py` 에 Comment 클래스를 만든다.

```python
class Comment(models.Model):
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    # ForeignKey 안에 들어갈 요소: 참조할 클래스 이름, on_delete
    # on_delete=models.CASCADE << 하나를 삭제했을 때 연관된 것을 다 삭제해야 DB에서 무결성을 유지하기 때문에
    # 즉, 원문이 삭제되면 그 안의 모든 댓글도 삭제해야 하므로

    class Meta:
        ordering = ['-pk',]   # 가장 마지막에 생성된 댓글을 맨 위에 출력하도록

    def __str__(self):
        return self.content
```

* ForeignKey 안에 들어갈 요소: 참조할 클래스 이름, on_delete
* `on_delete=models.CASCADE` 로 설정하는 이유는 하나를 삭제했을 때 연관된 것을 다 삭제해야 DB에서 무결성을 유지하기 때문에
  * 간단히 말해, 원문이 삭제되면 그 안의 모든 댓글도 삭제해야 하므로

bash에서 변경된 model을 migrate 해준다.

```bash
python manage.py makemigrations
python manage.py migrate
```

migration이 잘 됐는지 확인해볼 수 있다

```bash
python manage.py showmigrations
```

DB에서도 확인할 수 있다

```bash
sqlite3 db.sqlite3
```

```sqlite
sqlite> .tables
articles_article            auth_user_user_permissions
articles_comment            django_admin_log
auth_group                  django_content_type
auth_group_permissions      django_migrations
auth_permission             django_session
auth_user                   jobs_job
auth_user_groups

sqlite> .schema articles_comment
CREATE TABLE IF NOT EXISTS "articles_comment" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "conten
t" varchar(200) NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "article_id"
integer NOT NULL REFERENCES "articles_article" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE INDEX "articles_comment_article_id_59ff1409" ON "articles_comment" ("article_id");

sqlite> .exit
```

`django_crud` > `articles` > `models.py` 에서 댓글 출력되는 방식을 수정한다.

```python
class Comment(models.Model):
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-pk',]

    def __str__(self):    # 여기 수정
        return f'<Article({self.article_id}): Comment({self.pk}) - {self.content}>'
        # ex) <Article(1): Comment(1) - 제목내용>
```

* 이거 수정한거는 migrate 안해도 된다. 가장 상위 class에 변경이 있을때만 migrate 해야한다고 강사님께서 말씀하셨다.

shell에서 comment에 자료를 넣어볼건데, 더 편하게 사용하기 위해 django-extensions의 shell_plus를 쓰려고 한다.

우선 bash에서 django-extensions을 설치한다.

```bash
pip install django-extensions
```

`django_crud` > `crud` > `settings.py` 에 django-extensions을 추가한다.

```python
INSTALLED_APPS = [
    'jobs',
    'articles',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',    # 이거 추가
]
```

* INSTALLED_APPS에 쓸 때는 "django-extensions"가 아니라 "django_extensions"인 점에 주의한다.

bash에서 shell_plus를 실행한다.

```bash
python manage.py shell_plus
```

```shell
>>> article = Article.objects.get(pk=1)

# 첫번째 댓글 만들기
>>> article = Article.objects.get(pk=1)
>>> comment = Comment()
>>> comment.content = "first comment"
>>> comment.article = article    # article에 이어준 것 (foreign key 이용)
>>> comment.save()

# 만들어진 댓글 확인
>>> comment.pk
1
>>> comment.content
'first comment'
>>> comment.article_id
1
>>> comment
<Comment: <Article(1): Comment(1) - first comment>>

# 첫번째 댓글이 달린 게시글의 주소(pk)
>>> comment.article.pk
1

# 첫번째 댓글이 달린 게시글의 내용
>>> comment.article.content
'내용이에요'

# 두번째 댓글 달기
>>> comment = Comment(article=article, content="second comment")
>>> comment.save()
>>> comment.pk
2
>>> comment
<Comment: <Article(1): Comment(2) - second comment>>

# 이번엔 article의 입장에서 댓글 가져오기
>>> article = Article.objects.get(pk=1)
>>> article
<Article: 제목이에요>
>>> article.comment_set.all()
<QuerySet [<Comment: <Article(1): Comment(2) - second comment>>, <Comment: <Article(1): Comment(1) - first comment>>]>

>>> exit()
```

댓글들을 불러오기 편하게 하기 위해서 `django_crud` > `articles` > `models.py` 를 수정한다.

```python
class Comment(models.Model):
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # 기존
    # article = models.ForeignKey(Article, on_delete=models.CASCADE)
    
    # 변경 후
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments")

    # related_name을 설정해주므로써 댓글들 불러오는 코드가 바뀐다.
    # 기존 댓글을 불러올 때는: article.comment_set.all()
    # related_name 변경 후에는: article.comments.all()

    class Meta:
        ordering = ['-pk',]   # 가장 마지막에 생성된 댓글을 맨 위에 출력하도록

    def __str__(self):
        return f'<Article({self.article_id}): Comment({self.pk}) - {self.content}>'
        # ex) <Article(1): Comment(1) - 제목내용>
```

* related_name을 설정해주므로써 댓글들을 불러오는 코드를 더 편하게 쓸 수 있다.

게시물 상세 페이지에서 댓글들이 보이게끔 하려고 한다.

우선 `django_crud` > `articles` > `views.py` 에서 detail 메소드를 수정한다.

```python
def detail(request, pk):
    article = Article.objects.get(pk=pk)

    # article의 모든 댓글 가져오기
    # related_name 설정했을 시, comments로 가져와야 합니다.
    comments = article.comments.all()

    context = {
        'article': article,
        'comments': comments
    }
    return render(request, 'articles/detail.html', context)
```

`django_crud` > `articles` > `templates` > `articles` > `detail.html` 수정.

```html
<!-- templates/articles/detail.html -->

{% extends 'base.html' %}

{% block content %}

    ...

    <hr>
    <h3>Comments</h3>
    {% for comment in comments %}
        <p>{{ comment.pk }}. {{ comment.content }}</p>
        {% empty %}
            <p>댓글이 없습니다.</p>
    {% endfor %}

{% endblock %}
```



## 댓글 쓰기

`django_crud` > `articles` > `views.py` 에 댓글을 쓰기 위한 메소드 comment_create를 만든다.

```python
def comment_create(request, pk):
    
    # 댓글을 달 게시물
    article = Article.objects.get(pk=pk)

    if request.method =="POST":
        # form에서 넘어온 댓글 정보
        content = request.POST.get('content')
        if content == "":    # 댓글에 입력 내용 없으면 그냥 넘기기
            return redirect(article)
        else:
            # 댓글 생성 및 저장 후 리턴
            comment = Comment.objects.create(content=content, article=article)
            return redirect(article)

    else:
        # 원래는
        # return redirect("articles:detail", article.pk)
        # 이렇게 써야 하는데
        # get_absolute_url을 설정했기 때문에
        # 아래와 같이 쓴다.
        return redirect(article)
```

* else일 때는 method가 POST가 아닌 경우

`django_crud` > `articles` > `templates` > `articles` > `detail.html` 에 댓글 쓸 칸을 만든다.

```html
<!-- templates/articles/detail.html -->

{% extends 'base.html' %}

{% block content %}

    ...

    <!-- <hr>
    <h3>Comments</h3>
    {% for comment in comments %}
        <p>{{ comment.pk }}. {{ comment.content }}</p>
        {% empty %}
            <p>댓글이 없습니다.</p>
    {% endfor %} -->
    <!-- 위와 같이 하니까 서로 다른 게시물에서도 댓글 앞에 붙는 번호가 계속 증가해서 (pk니까) 보기 안좋아서 아래와 같이 변경 -->

    <hr>
    <h3>Comments</h3>
    <ol reversed>    <!-- 댓글을 (models.py에서) 최신 댓글이 맨 위로 오도록 설정했으므로 번호도 거꾸로 붙게 설정한다 -->
        {% for comment in comments %}
            <li>{{ comment.content }}</li>
            {% empty %}
                <p>댓글이 없습니다.</p>
        {% endfor %}
    </ol>

    <hr>
    <h3>Create Comment</h3>
    <form action="{% url 'articles:comment_create' article.pk %}" method="POST">
        {% csrf_token %}
        <textarea name="content" id="" cols="30" rows="10"></textarea>
        <input type="submit" value="submit comment">
    </form>

{% endblock %}
```

`django_crud` > `articles` > `urls.py` 수정.

```python
urlpatterns = [
    ...
    path('<int:pk>/comments', views.comment_create, name="comment_create")
]
```



## 관리자 페이지에서 댓글 목록 보이게 하기

`django_crud` > `articles` > `admin.py` 수정.

```python
from .models import Article, Comment
...
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'content', 'created_at', 'updated_at')
...
admin.site.register(Comment, CommentAdmin)
```



## 댓글 삭제하기

`django_crud` > `articles` > `views.py` 에 comment_delete 메소드 추가.

```python
def comment_delete(request, article_pk, comment_pk):
    if request.method == "POST":
        comment = Comment.objects.get(pk=comment_pk)
        comment.delete()
        return redirect('articles:detail', article_pk)
    else:
        return redirect('articles:detail', article_pk)
```

* 댓글을 삭제할 때는 article의 pk와 comment의 pk가 모두 필요하다.

`django_crud` > `articles` > `urls.py` 에 경로 추가.

```python
urlpatterns = [
    ...
    path('<int:article_pk>/comments/<int:comment_pk>/delete/', views.comment_delete, name="comment_delete")
]
```

`django_crud` > `articles` > `templates` > `articles` > `detail.html` 수정.

```html
...
<hr>
<h3>Comments</h3>
<ol reversed>
    {% for comment in comments %}
        <li>{{ comment.content }}</li>
        <form action="{% url 'articles:comment_delete' article.pk comment.pk %}" method="POST">
            {% csrf_token %}
            <input type="submit" value="DELETE">
        </form>
        {% empty %}
        	<p>댓글이 없습니다.</p>
    {% endfor %}
</ol>
...
```



## 댓글 개수 출력하기

`django_crud` > `articles` > `templates` > `articles` > `detail.html` 수정.

```html
...
<!-- 댓글 목록 -->

<hr>
<h3>Comments</h3>

<!-- 댓글 개수 -->
    <!-- 3가지 방법 -->
    <!-- {{ comments | length }} -->
    <!-- {{ article.comments.all | length }} -->
    <!-- {{ comments.count }} -->
<h6>{{ comments | length }}개의 댓글이 있습니다.</h5>

<ol reversed>
    {% for comment in comments %}
        <li>{{ comment.content }}</li>
        <form action="{% url 'articles:comment_delete' article.pk comment.pk %}" method="POST">
            {% csrf_token %}
            <input type="submit" value="DELETE">
        </form>
        {% empty %}
        	<p>댓글이 없습니다.</p>
    {% endfor %}
</ol>
...
```

* 댓글 개수를 표시하는데는 3가지 방법이 있다
  * {{ comments | length }}
  * {{ article.comments.all | length }}
  * {{ comments.count }}
* 근데 위의 두개를 사용하길 권장한다. 왜냐하면 마지막 코드는 성능이 떨어지기 때문이다.



# 마무리: requirements 만들어주기

```bash
pip freeze > requirements.txt
```

