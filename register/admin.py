from django.contrib import admin
from .models import User, AppUsers
# Register your models here.
admin.site.register(AppUsers)
admin.site.register(User)