from django.db import models

# Create your models here.

class Item(models.Model):
    modelnum = models.TextField()    # 연결될 모델명
    productName = models.TextField()    # 제품명
    retailer = models.TextField()    # 사이트명
    link = models.TextField()    # 링크
    thumbnail_url = models.TextField(null=True)    # 썸네일
    price = models.TextField()    # 가격
    reviewnum = models.TextField(null=True)    # 리뷰 개수
    rating = models.TextField(null=True)    # 별점