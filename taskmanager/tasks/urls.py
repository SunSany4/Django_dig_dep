from django.urls import path
from .views import register, user_login, user_logout, tasks

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('tasks/', tasks, name='tasks'),
]