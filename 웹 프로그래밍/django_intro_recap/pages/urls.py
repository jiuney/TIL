# pages/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('throw/', views.throw),
    path('catch/', views.catch),
    path('lotto_pick/', views.lotto_pick),
    path('lotto_get/', views.lotto_get),
    path('lottery/', views.lottery),
    path('jackpot/', views.jackpot),
    path('user_new/', views.user_new),
    path('user_create/', views.user_create),
    path('static_example/', views.static_example)
]