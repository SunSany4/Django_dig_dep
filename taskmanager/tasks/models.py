from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords

class Category(models.Model):
    name = models.CharField(max_length=200, unique=True);

    def __str__(self):
        return self.name    

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.title
