from django.db import models
from django.conf import settings

# Create your models here.

class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    poster = models.ImageField(blank=True, upload_to='movies/%Y/%m/%d')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-pk',)
    
    def __str__(self):
        return self.title

class Rating(models.Model):
    score = models.FloatField()
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-pk',)

    def __str__(self):
        return self.content