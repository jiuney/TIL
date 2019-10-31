from django.shortcuts import render, redirect
from .models import Article, Comment

# Create your views here.

def index(request):
    articles = Article.objects.all()
    context = {
        'articles': articles
    }
    return render(request, 'articles/index.html', context)

''' new 메소드를 삭제해 주고 create와 합쳐준다.
def new(request):
    return render(request, 'articles/new.html')

def create(request):
    title = request.POST.get("title")
    content = request.POST.get("content")
    Article.objects.create(title=title, content=content)
    return redirect('/articles/')
'''

def create(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        article = Article.objects.create(title=title, content=content)
        return redirect('articles:detail', article.pk)
    else:
        return render(request, 'articles/new.html')

def detail(request, pk):
    article = Article.objects.get(pk=pk)

    # article의 모든 댓글 가져오기
    # related_name 설정했을 시, comments로 가져와야 합니다.
    comments = article.comments.all()

    context = {
        'article': article,
        'comments': comments
    }
    return render(request, 'articles/detail.html', context)

'''
def delete(request, pk):
    article = Article.objects.get(pk=pk)
    article.delete()
    return redirect('/articles/')
'''

def delete(request, pk):
    article = Article.objects.get(pk=pk)
    if request.method == "POST":
        article.delete()
        return redirect('articles:index')
    else:
        # return redirect('articles:detail', article.pk)  # before
        return redirect(article)  # after

''' edit 메소드를 삭제해주고 update와 합쳐준다.
def edit(request, pk):
    article = Article.objects.get(pk=pk)
    context = {
        'article': article
    }
    return render(request, 'articles/edit.html', context)

def update(request, pk):
    article = Article.objects.get(pk=pk)
    title = request.POST.get('title')
    content = request.POST.get('content')

    article.title = title
    article.content = content

    article.save()

    return redirect('/articles/')
'''

def update(request, pk):
    article = Article.objects.get(pk=pk)
    if request.method =="POST":
        title = request.POST.get('title')
        content = request.POST.get('content')

        article.title = title
        article.content = content

        article.save()

        return redirect('articles:index')
    else:
        context = {
            'article': article
        }
        return render(request, 'articles/update.html', context)

def comment_create(request, pk):
    
    # 댓글을 달 게시물
    article = Article.objects.get(pk=pk)

    if request.method =="POST":
        # form에서 넘어온 댓글 정보
        content = request.POST.get('content')
        if content == "":    # 댓글에 입력 내용 없으면 그냥 넘기기
            return redirect(article)
        else:
            # 댓글 생성 및 저장 후 리턴
            comment = Comment.objects.create(content=content, article=article)
            return redirect(article)

    else:
        return redirect(article)

def comment_delete(request, article_pk, comment_pk):
    if request.method == "POST":
        comment = Comment.objects.get(pk=comment_pk)
        comment.delete()
        return redirect('articles:detail', article_pk)
    else:
        return redirect('articles:detail', article_pk)