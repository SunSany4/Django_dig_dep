from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, TaskForm
from .models import Task,  Category


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

#TODO: сделать кнопку админки доступной только для админов, сделать переходд после логина на домашнюю страницу
@login_required
def tasks(request):
    category_id = request.GET.get('category')
    status = request.GET.get('status')
    tasks = Task.objects.filter(user=request.user)

    if category_id:
        tasks = tasks.filter(category_id=category_id)

    if status == 'completed':
        tasks = tasks.filter(completed=True)
    elif status == 'incomplete':
        tasks = tasks.filter(completed=False)

    categories = Category.objects.all()

    return render(request, 'tasks/task_list.html', {'tasks': tasks, 'categories': categories})

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


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})


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