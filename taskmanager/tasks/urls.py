from django.urls import path
from .views import register, user_login, user_logout, tasks, create_task, edit_task, delete_task

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('tasks/', tasks, name='tasks'),
    path('tasks/new', create_task, name='create_task'),
    path('tasks/edit/<int:task_id>', edit_task, name='edit_task'),
    path('tasks/delete/<int:task_id>', delete_task, name='delete_task'),
]