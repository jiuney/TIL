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