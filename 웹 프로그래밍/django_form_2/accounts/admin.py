from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from .models import User
from django.contrib.auth.models import User
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = [f.name for f in User._meta.fields]

admin.site.register(User, UserAdmin)