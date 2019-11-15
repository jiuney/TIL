from django.contrib import admin
from .models import Movie, Rating

# Register your models here.

class MovieAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'user')

class RatingAdmin(admin.ModelAdmin):
    list_display = ('pk', 'score', 'user')

admin.site.register(Movie, MovieAdmin)
admin.site.register(Rating, RatingAdmin)