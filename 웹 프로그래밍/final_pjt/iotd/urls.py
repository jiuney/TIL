from django.urls import path
from . import views

app_name = 'iotd'

urlpatterns = [
    path('', views.index, name="index"),
    path('detail/', views.detail, name="detail"),
    path('crawling/', views.crawling, name="crawling")
]