from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.paginator import Paginator

from .forms import RegisterForm, TaskForm
from .models import Task,  Category
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .serializers import TaskSerializer



class TaskListCreate(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        tasks = Task.objects.filter(user=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetail(APIView):
    def get_object(self, id, user):
        task = get_object_or_404(Task, id=id, user=user)
        return task 

    def get(self, request, id):
        task = self.get_object(id, request.user)
        serializer = TaskSerializer(task)
        return Response(serializer.data)
    
    def put(self, request, id):
        task = self.get_object(id, request.user)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        task = self.get_object(id, request.user)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    # def delete(self, request, id):
    #     task = get_object_or_404(Task, id=id)
    #     task.delete()
    #     return Response(status=status.HTTP_200_OK)

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, "tasks/register.html", {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('tasks')
    return render(request, 'tasks/login.html')

def user_logout(request):
    logout(request)
    return redirect('home')

#TODO: сделать кнопку админки доступной только для админов, сделать переход после логина на домашнюю страницу, комментарии к задачам, логирование, уровни доступа пользователей к задачам
#TODO: исторю изменений, прикрутить визуал, API, прикртутить файлы,
@login_required
def tasks(request):
    category_id = request.GET.get('category')
    status = request.GET.get('status')
    query = request.GET.get('q', '')
    if query:
       tasks = Task.objects.filter(title__icontains=query)
    else:
        tasks = Task.objects.all()
    paginator = Paginator(tasks, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    

    if category_id:
        tasks = tasks.filter(category_id=category_id)

    if status == 'completed':
        tasks = tasks.filter(completed=True)
    elif status == 'incomplete':
        tasks = tasks.filter(completed=False)

    # categories = Category.objects.all()

    # return render(request, 'tasks/task_list.html', {'tasks': tasks, 'categories': categories})
    return render(request, 'tasks/task_list.html', {'page_obj': page_obj, 'query':  query})

@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('tasks')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})

@csrf_exempt
def create_task_ajax(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        category = Category.objects.get(id=category_id) if category_id else None


        task = Task.objects.create(
            title=title,
            description=description,
            category_id=category_id,
            user=request.user
        )

        return JsonResponse({'success': True,
                            'task_id': task.id,
                            "title": task.title,
                            "description": task.description,
                            "category": category.name if category else "Без категории"
                            })

    return JsonResponse({'success': False})

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, f'Задача {task.title} успешно обновлена')
            return redirect('tasks')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form})

@csrf_exempt
def edit_task_ajax(request, task_id):
    if request.method == 'POST':
        try:
            task = Task.objects.get(id=task_id)
            task.title = request.POST.get('title')
            task.description = request.POST.get('description')
            task.category_id = request.POST.get('category')
            task.save()
            return JsonResponse({'success': True,
                                'task_id': task.id,
                                "title": task.title,
                                "description": task.description,
                                # "category": category.name if category else "Без категории"
                                })
        except Task.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Task not found'})
    return JsonResponse({"success" : False, "error" : "Invalid request method"})

@csrf_exempt
def delete_task_ajax(request, task_id):
    if request.method == 'POST':
        try:
            task = Task.objects.get(id=task_id)
            task.delete()
            return JsonResponse({'success': True})
        except Task.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Task not found'})
    return JsonResponse({"success" : False, "error" : "Invalid request method"})

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})


@csrf_exempt
def completed_task_ajax(request, task_id):
    if request.method == 'POST':
        try:
            task = Task.objects.get(id=task_id)
            task.completed = True
            task.save()
            return JsonResponse({'success': True})
        except Task.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Task not found'})
    return JsonResponse({"success" : False})

@csrf_exempt
def incomplete_task_ajax(request, task_id):
    if request.method == 'POST':
        try:
            task = Task.objects.get(id=task_id)
            task.completed = False
            task.save()
            return JsonResponse({'success': True})
        except Task.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Task not found'})
    return JsonResponse({"success" : False})

def home(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('tasks')
        else: 
            messages.error(request, 'Неправильный логин или пароль')
    return render(request, 'tasks/home.html')