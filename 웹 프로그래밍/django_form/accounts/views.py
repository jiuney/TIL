from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.views.decorators.http import require_POST
from .forms import CustomUserChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

# Create your views here.

def signup(request):

    if request.user.is_authenticated:
        return redirect('articles:index')
    
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('articles:index')
    else:
        form = UserCreationForm()
    context = {'form': form}
    return render(request, 'accounts/auth_form.html', context)

def login(request):

    if request.user.is_authenticated:
        return redirect('articles:index')

    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'articles:index')
    else:
        form = AuthenticationForm()
    context = {'form': form}
    return render(request, 'accounts/auth_form.html', context)

def logout(request):
    auth_logout(request)
    return redirect('articles:index')

@require_POST
def delete(request):
    request.user.delete()
    return redirect('articles:index')

@login_required
def update(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('articles:index')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {'form': form}
    return render(request, 'accounts/auth_form.html', context)

@login_required
def change_password(request):
    if request.method == "POST":
        # 반드시 user정보(request.user)를 먼저 작성해주세요.
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            # 현재 사용자의 인증 세션이 무효화되는 것을 막고,
            # 세션을 유지한 상태로 비밀번호를 업데이트 시켜준다.
            update_session_auth_hash(request, form.user)
            return redirect('articles:index')
    else:
        form = PasswordChangeForm(request.user)
    context = {'form': form}
    return render(request, 'accounts/auth_form.html', context)