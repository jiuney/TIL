from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import MovieForm, RatingForm
from .models import Movie, Rating

# Create your views here.

def index(request):
    return render(request, 'movies/index.html')

@login_required
def new(request):

    if request.method == "POST":
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.user = request.user
            movie.save()
            return redirect('movies:index')
    
    else:
        form = MovieForm()
    
    context = {'form': form}
    return render(request, 'movies/new.html', context)

def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    context = {
        'movie': movie
    }
    return render(request, 'movies/detail.html', context)

@login_required
def edit(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.user == movie.user:
        pass
    else:
        return redirect('movies:detail', movie_pk)