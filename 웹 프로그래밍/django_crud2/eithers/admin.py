from django.contrib import admin
from .models import Question, Answer

# Register your models here.

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'issue_a', 'issue_b', 'image_a', 'image_b')

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('pk', 'question_id', 'pick')

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)