from django.contrib import admin
from .models import Movie

# Register your models here.

class MovieAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'genre')

admin.site.register(Movie, MovieAdmin)