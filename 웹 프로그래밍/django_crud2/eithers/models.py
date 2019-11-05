from django.db import models

# Create your models here.

class Question(models.Model):
    title = models.CharField(max_length=50)
    issue_a = models.CharField(max_length=200)
    issue_b = models.CharField(max_length=200)
    image_a = models.ImageField(blank=True, upload_to="eithers/images")
    image_b = models.ImageField(blank=True, upload_to="eithers/images")

class Answer(models.Model):
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    pick = models.IntegerField()
    comment = models.TextField()