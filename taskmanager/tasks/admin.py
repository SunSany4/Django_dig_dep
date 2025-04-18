from django.contrib import admin
from .models import Task, Category
from simple_history.admin import SimpleHistoryAdmin
# Register your models here.



admin.site.register(Task)
admin.site.register(Category)