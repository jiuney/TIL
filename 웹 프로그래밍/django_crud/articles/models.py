from django.db import models
from django.urls import reverse

# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        # ex) 'articles/10/'
        return reverse('articles:detail', args=[str(self.pk)])

class Comment(models.Model):
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments")

    class Meta:
        ordering = ['-pk',]   # 가장 마지막에 생성된 댓글을 맨 위에 출력하도록

    def __str__(self):
        return f'<Article({self.article_id}): Comment({self.pk}) - {self.content}>'
        # ex) <Article(1): Comment(1) - 제목내용>