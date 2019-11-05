from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail

# Create your models here.

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