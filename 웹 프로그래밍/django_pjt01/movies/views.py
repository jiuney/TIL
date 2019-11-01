from django.shortcuts import render, redirect
from .models import Movie

# Create your views here.

def index(request):
    movies = Movie.objects.all()
    context = {
        'movies': movies
    }
    return render(request, 'movies/index.html', context)

def create(request):
    if request.method == "POST":
        title = request.POST.get('title')
        title_en = request.POST.get('title_en')
        audience = request.POST.get('audience')
        if audience == "":
            audience = None
        open_date = request.POST.get('open_date')
        if open_date == "":
            open_date = None
        genre = request.POST.get('genre')
        watch_grade = request.POST.get('watch_grade')
        score = request.POST.get('score')
        if score == "":
            score = None
        poster_url = request.POST.get('poster_url')
        description = request.POST.get('description')

        movie = Movie()
        movie.title = title
        movie.title_en = title_en
        movie.audience = audience
        movie.open_date = open_date
        movie.genre = genre
        movie.watch_grade = watch_grade
        movie.score = score
        movie.poster_url = poster_url
        movie.description = description
        movie.save()

        context = {
            'movie': movie
        }

        return render(request, 'movies/detail.html', context)

    else:
        return render(request, 'movies/create.html')

def detail(request, pk):
    movie = Movie.objects.get(pk=pk)
    context = {
        'movie': movie
    }
    return render(request, 'movies/detail.html', context)

def edit(request, pk):
    movie = Movie.objects.get(pk=pk)
    if request.method == "POST":
        title = request.POST.get('title')
        title_en = request.POST.get('title_en')
        audience = request.POST.get('audience')
        if audience == "":
            audience = None
        open_date = request.POST.get('open_date')
        if open_date == "":
            open_date = None
        genre = request.POST.get('genre')
        watch_grade = request.POST.get('watch_grade')
        score = request.POST.get('score')
        if score == "":
            score = None
        poster_url = request.POST.get('poster_url')
        description = request.POST.get('description')

        movie.title = title
        movie.title_en = title_en
        movie.audience = audience
        movie.open_date = open_date
        movie.genre = genre
        movie.watch_grade = watch_grade
        movie.score = score
        movie.poster_url = poster_url
        movie.description = description

        movie.save()

        context = {
            'movie': movie
        }

        return render(request, 'movies/detail.html', context)
    else:
        context = {
            'movie': movie
        }
        return render(request, 'movies/edit.html', context)

def delete(request, pk):
    movie = Movie.objects.get(pk=pk)
    if request.method == "POST":
        movie.delete()
        return redirect('movies:index')
    else:
        return redirect('movies:index')