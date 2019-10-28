# utilities/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('asciify/', views.asciify),
    path('asciify2/', views.asciify2),
    path('asciify2_art/', views.asciify2_art)
]