from django.db import models

# Create your models here.

class Movie(models.Model):
    title = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200)
    audience = models.IntegerField(blank=True, null=True)
    open_date = models.DateField(blank=True, null=True)
    genre = models.CharField(max_length=50, blank=True)
    watch_grade = models.CharField(max_length=25, blank=True)
    score = models.FloatField(blank=True, null=True)
    poster_url = models.TextField(blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title