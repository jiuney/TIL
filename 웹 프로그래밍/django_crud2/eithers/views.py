from django.shortcuts import render, redirect
from .models import Question, Answer

# Create your views here.

def index(request):
    questions = Question.objects.all()
    context = {
        'questions': questions
    }
    return render(request, 'eithers/index.html', context)

def create(request):
    if request.method == "POST":
        title = request.POST.get('title')
        issue_a = request.POST.get('issue_a')
        issue_b = request.POST.get('issue_b')
        image_a = request.FILES.get('image_a')
        image_b = request.FILES.get('image_b')
        Question.objects.create(
            title = title,
            issue_a = issue_a,
            issue_b = issue_b,
            image_a = image_a,
            image_b = image_b
        )
        return redirect('eithers:index')
    else:
        return render(request, 'eithers/new.html')

def detail(request, question_pk):
    question = Question.objects.get(pk=question_pk)
    answers = Answer.objects.filter(question_id=question)
    context = {
        'question': question,
        'answers': answers
    }
    return render(request, 'eithers/detail.html', context)