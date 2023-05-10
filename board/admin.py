from django.contrib import admin
from .models import Category, Task, Success_task

# Register your models here.
admin.site.register(Category)
admin.site.register(Task)
admin.site.register(Success_task)