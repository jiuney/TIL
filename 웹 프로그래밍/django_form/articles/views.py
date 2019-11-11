from django.shortcuts import render, redirect, get_object_or_404
from .models import Article, Comment
from .forms import ArticleForm, CommentForm
from django.views.decorators.http import require_POST
from IPython import embed
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Create your views here.
def index(request):
    articles = Article.objects.all()
    context = {'articles': articles}
    return render(request, 'articles/index.html', context)

# 이런 식으로도 사용 가능하다! @login_required(login_url="/accounts/test/")
@login_required
def create(request):
    if request.method == "POST":
        # 폼 인스턴스를 생성하고 요청에 의한 데이터로 채운다. (binding)
        form = ArticleForm(request.POST)
        # 폼이 유효한지 체크한다.
        if form.is_valid():
            article = form.save(commit=False)
            # title = form.cleaned_data.get("title")
            # content = form.cleaned_data.get("content")
            # article = Article(title=title, content=content)
            # article.save()
            article.user = request.user
            article.save()
            return redirect("articles:detail", article.pk)
    else:
        form = ArticleForm()
    context = {'form': form}
    return render(request, 'articles/create.html', context)

def detail(request, article_pk):
    # article = Article.objects.get(pk=article_pk)
    article = get_object_or_404(Article, pk=article_pk)
    comments = Comment.objects.filter(article=article)
    comment_form = CommentForm()
    context = {'article': article, 'comment_form': comment_form, 'comments': comments}
    return render(request, 'articles/detail.html', context)

@require_POST
def delete(request, article_pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Article, pk=article_pk)
        if request.user == article.user:
            article.delete()
        return redirect("articles:index")
    return HttpResponse("You are Unauthorized", status=401)

@login_required
def update(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.user == article.user:
        if request.method == "POST":
            form = ArticleForm(request.POST)
            form = ArticleForm(request.POST, instance=article)
            if form.is_valid():
                form.save()
                # article.title = form.cleaned_data.get("title")
                # article.content = form.cleaned_data.get("content")
                # article.save()
                return redirect("articles:detail", article_pk)
        else:
            form = ArticleForm(instance=article)
    else:
        return redirect('articles:index')
    context = {'form': form}
    return render(request, 'articles/create.html', context)

@require_POST
def comments_create(request, article_pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Article, pk=article_pk)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.article = article
            comment.user = request.user
            comment.save()
        return redirect("articles:detail", article_pk)
    return HttpResponse("You are Unauthorized", status=401)

@require_POST
def comments_delete(request, article_pk, comment_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_pk)
        if request.user == comment.user:
            comment.delete()
        return redirect("articles:detail", article_pk)
    return HttpResponse("You are Unauthorized", status=401)