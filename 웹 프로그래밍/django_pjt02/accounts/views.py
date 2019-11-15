from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.views.decorators.http import require_POST

# Create your views here.

def signup(request):

    if request.user.is_authenticated:
        return redirect('movies:index')
    
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, '회원으로 가입되셨습니다.')
            auth_login(request, user)
            return redirect('movies:index')
    
    else:
        form = UserCreationForm()

    context = {'form': form}
    return render(request, 'accounts/auth_form.html', context)

def signout(request):
    auth_logout(request)
    return redirect('movies:index')

def signin(request):
    
    if request.user.is_authenticated:
        return redirect('movies:index')
    
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'movies:index')

    else:
        form = AuthenticationForm()
    
    context = {'form': form}
    return render(request, 'accounts/auth_form.html', context)

@require_POST
def delete(request):
    request.user.delete()
    return redirect('movies:index')