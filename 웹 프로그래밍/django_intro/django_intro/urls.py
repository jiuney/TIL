"""django_intro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from pages import views    # 생성한 앱 pages 폴더 안의 view.py 파일

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index),    # django에서는 url 경로 마지막에 "/"를 붙여야 한다.
    path('introduce/<str:name>/<int:age>/', views.introduce),
    path('dinner/', views.dinner),
    path('image/', views.image),
    path('hello/<str:name>/', views.hello),    # hello/ 뒤에 오는 내용을 str으로 name이란 변수에 저장할 것이라는 뜻.
    path('times/<int:num1>/<int:num2>/', views.times),
    path('circle/<int:radius>/', views.circle),    # 반지름을 인자로 받아서 원의 넓이를 구해주세요!
    path('template_language/', views.template_language),
    path('isbirth/', views.isbirth),
    path('ispal/<str:input>', views.ispal)
]
