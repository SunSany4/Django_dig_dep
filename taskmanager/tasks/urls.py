from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('tasks/', tasks, name='tasks'),
    path('tasks/new', create_task, name='create_task'),
    path('tasks/create/', create_task_ajax, name='create_task_ajax'),
    path('tasks/delete_ajax/<int:task_id>', delete_task_ajax, name='delete_task_ajax'),
    path('tasks/edit/<int:task_id>', edit_task, name='edit_task'),
    path('tasks/edit_ajax/<int:task_id>', edit_task_ajax, name='edit_task_ajax'),
    path('tasks/delete/<int:task_id>', delete_task, name='delete_task'),
    path('tasks/complete/<int:task_id>', completed_task_ajax, name='completed_task_ajax'),
    path('tasks/incomplete/<int:task_id>', incomplete_task_ajax, name='incomplete_task_ajax'),
    path('api/tasks/', TaskListCreate.as_view(), name='api-task-list-create'),
    path('api/tasks/<int:id>', TaskDetail.as_view(), name='api-task-detail'),
    path('api/token/', obtain_auth_token, name='api-auth-token')
]