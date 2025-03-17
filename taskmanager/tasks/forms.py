from django import forms
from .models import Task, Category
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class TaskForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                      required=False,
                                      empty_label='Категория не выбрана')
    class Meta:
        model = Task
        fields = ['title', 'description', 'completed', 'category']


