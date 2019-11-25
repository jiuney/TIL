from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Article, Comment, Hashtag
from .forms import ArticleForm, CommentForm
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from IPython import embed
import hashlib

# Create your views here.
def index(request):
    articles = Article.objects.all()
    paginator = Paginator(articles, 3) # 한 페이지에 몇 개 보여줄지 설정
    page = request.GET.get("page") # 페이지 번호
    articles = paginator.get_page(page) # 해당 번호의 페이지에서 게시글 가져오기

    context = {
        'articles': articles,
    }
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
            article.user = request.user
            article.save()
            messages.success(request, '게시글이 성공적으로 작성되었습니다!')
            # hashtag
            for word in article.content.split():
                if word.startswith("#"):
                    hashtag, created = Hashtag.objects.get_or_create(content=word)
                    article.hashtags.add(hashtag)
            return redirect("articles:detail", article.pk)
    else:
        form = ArticleForm()
    context = {'form': form}
    return render(request, 'articles/create.html', context)


def detail(request, article_pk):
    # article = Article.objects.get(pk=article_pk)
    article = get_object_or_404(Article, pk=article_pk)
    comments = Comment.objects.filter(article=article)
    person = get_object_or_404(get_user_model(), pk=article.user_id)
    comment_form = CommentForm()
    context = {
        'article': article, 
        'comment_form': comment_form, 
        'comments': comments,
        'person': person,
    }
    return render(request, 'articles/detail.html', context)


@require_POST
def delete(request, article_pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Article, pk=article_pk)
        if request.user == article.user:
            article.delete()
        return redirect("articles:index")
    return HttpResponse('You are Unauthorized', status=401)


@login_required
def update(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.user == article.user:
        if request.method == "POST":
            form = ArticleForm(request.POST, instance=article)
            if form.is_valid():
                article = form.save()
                # hashtag
                article.hashtags.clear()
                for word in article.content.split():
                    if word.startswith("#"):
                        hashtag, created = Hashtag.objects.get_or_create(content=word)
                        article.hashtags.add(hashtag)
                return redirect("articles:detail", article_pk)
        else:
            form = ArticleForm(instance=article)
    else:
        return redirect("articles:index")
    context = {'form': form}
    return render(request, 'articles/create.html', context)

@require_POST
def comments_create(request, article_pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Article, pk=article_pk)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user # 댓글 작성한 사용자 저장
            comment.article = article
            comment.save()
        return redirect("articles:detail", article_pk)
    return HttpResponse('You are Unauthorized', status=401)

@require_POST
def comments_delete(request, article_pk, comment_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_pk)
        if request.user == comment.user:
            comment.delete()
    return redirect("articles:detail", article_pk)


def like(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    user = request.user # 요청을 보낸 유저
    
    # 해당 게시글에 좋아요를 누른 사람들 중에
    # user.pk를 가진 유저가 존재하면,
    if request.user.is_authenticated:
        if article.like_users.filter(pk=user.pk).exists():
            # user를 삭제하고 (좋아요를 취소)
            article.like_users.remove(user)
            liked = False
        else:
            article.like_users.add(user)
            liked = True
        context = {'liked': liked}
        return JsonResponse(context)
    return redirect("accounts:login")


@login_required
def follow(request, article_pk, user_pk):
    # 게시글 유저
    you = get_object_or_404(get_user_model(), pk=user_pk)
    # 현재 접속 유저
    me = request.user
    if you != me:
        if you.followers.filter(pk=me.pk).exists():
            you.followers.remove(me)
        else:
            you.followers.add(me)
    return redirect("articles:detail", article_pk)


def hashtag(request, hash_pk):
    hashtag = get_object_or_404(Hashtag, pk=hash_pk)
    articles = hashtag.article_set.order_by("-pk")
    context = {'hashtag': hashtag, 'articles': articles}
    return render(request, 'articles/hashtag.html', context)


def search(request):
    # 사용자 검색어 추출
    query = request.GET.get("query")
    # 제목 또는 내용에서 검색어를 포함하는 게시글 가져오기
    # from django.db.models import Q
    articles = Article.objects.filter(
        Q(title__icontains=query) | Q(content__icontains=query)
    )
    
    # 페이지네이션 코드
    paginator = Paginator(articles, 3)
    page = request.GET.get("page")
    articles = paginator.get_page(page)

    context = {'articles': articles}
    return render(request, 'articles/search.html', context)