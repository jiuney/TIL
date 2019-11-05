



어제 만든 프로젝트와 앱에서 이어서



================== 이미지 사이즈 조절 ==================



필요한 모듈

```bash
pip install Pillow
pip install pilkit
pip install django-imagekit
```



프로젝트폴더 settings.py에 추가

```python
INSTALLED_APPS = [
    ...
    'imagekit',
]
```



articles > models.py

```python
...
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail

...

class Article(models.Model):
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # image = models.ImageField(blank=True, upload_to="articles/%Y/%m/%d")    # ImageField는 pillow 필수
    image = ProcessedImageField(
        processors=[Thumbnail(200, 300)],    # 처리할 작업 목록
        format='JPEG',    # 저장 포맷
        options={'quality': 90},    # 추가 옵션
        upload_to="articles/%Y/%m/%d"    # 저장 위치 (MEDIA_ROOT/articles/images)
    )
```



```bash
python manage.py makemigrations
python manage.py migrate
```



index.html에 게시물 작성하기 버튼 추가

```html
...
<h1>Articles!</h1>
<hr>
<a href="{% url 'articles:create' %}">[+ 새 게시물 작성하기]</a>
<hr>
...
```



서버 켜고 이미지 업로드 해보기

model에 적힌대로 처리된 이미지만 저장된 것을 알 수 있다.





================== favicon 만들기 ==================

[https://www.favicon-generator.org/](https://www.favicon-generator.org/) 에서 favicon 만들어서 다운로드하고 압축 풀기

앱 폴더인 articles 폴더 안에 static 폴더 안에 favicon 폴더 만들기

압축 푼 폴더에서 32x32.png 파일을 복사해서 favicon 폴더 안에 넣기

base.html 수정

```html
{% load static %}

...

<head>
    ...
    <link rel="icon" href="{% static 'favicon/favicon-32x32.png' %}" type="image/png">
    ...
</head>

...
```



================== 참고 ==================

A와 B가 모두 참일 때

val = A or B 인 경우 변수 val에는 A가 들어간다

val = A and B 인 경우 변수 val에는 B가 들어간다



























==================  ==================

























==================  ==================























==================  ==================

















==================  ==================





















































































































































































