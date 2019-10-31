from django.urls import path
from . import views

app_name = 'articles'    # 앱 이름 설정 - 이걸 해야 편하다

urlpatterns = [
    # # 기존 url
    # path('', views.index, name="index"),
    # path('new/', views.new, name="new"),
    # path('create/', views.create, name="create"),
    # path('detail/<int:pk>/', views.detail, name="detail"),
    # path('<int:pk>/delete/', views.delete, name="delete"),
    # path('<int:pk>/edit/', views.edit, name="edit"),
    # path('<int:pk>/update/', views.update, name="update")

    # 변경 후 url
    path('', views.index, name="index"),
    path('create/', views.create, name="create"),
    path('<int:pk>/', views.detail, name="detail"),
    path('<int:pk>/delete/', views.delete, name="delete"),
    path('<int:pk>/update/', views.update, name="update"),
    path('<int:pk>/comments', views.comment_create, name="comment_create"),
    path('<int:article_pk>/comments/<int:comment_pk>/delete/', views.comment_delete, name="comment_delete")
]