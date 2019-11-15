from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# Register your models here.

# UserAdmin.list_display = [f.name for f in User._meta.fields]
# print([f.name for f in User._meta.fields])
# ['id', 'password', 'last_login', 'is_superuser', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'date_joined']

UserAdmin.list_display = ('pk', 'id', 'username')