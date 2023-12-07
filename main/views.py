from django.shortcuts import render, redirect
from .models import Task, Date
from .forms import TaskForm
from datetime import date
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
            username = request.POST.get('username').lower()
            password = request.POST.get('password')
            try:
                user = User.objects.get(username=username)
            except:
                pass
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
            else:
                return redirect('login_user')
    return render(request, 'main/login.html', {})


def logout_user(request):
    logout(request)
    return redirect('login_user')


# Create your views here.
def home_(request):
    q = request.GET.get('q')
    if q:
        tasks = Task.objects.filter(completed=q)
    else:
        tasks = Task.objects.all()
    form = TaskForm()
    if request.method == 'POST':
        task = TaskForm(request.POST)
        if task.is_valid():
            task.save()
            return redirect('home')
    context = {'tasks': tasks, 'form':form}
    return render(request, 'main/index.html', context)

@login_required(login_url='login_user')
def home(request):
    q = request.GET.get('q')
    dates = Date.objects.all()
    if q:
        tasks = {f"{date_today}":date_today.task_set.filter(completed=q) for date_today in dates}
    else:
        tasks = {f"{date_today}":date_today.task_set.all() for date_today in dates}
    [d.delete() for d in dates if not d.task_set.all()]
    form = TaskForm()
    if request.method == 'POST':
        task = TaskForm(request.POST)
        if task.is_valid():
            task = task.save(commit=False)
            today = Date.objects.filter(now=date.today())
            today = Date.objects.get_or_create(now=date.today())
            if today:
                task.date = today[0]
            # else:
            #     task.date = Date.objects.create(now=date.today())
            task.save()
            return redirect('home')
    context = {'tasks': tasks, 'form':form}
    return render(request, 'main/index_copy.html', context)



def delete_task(request, pk):
    task = Task.objects.get(id=pk)
    task.delete()
    return redirect('home')


def complete_task(request, pk):
    task = Task.objects.get(id=pk)
    task.completed = not task.completed
    task.save()
    return redirect('home')



def edit_task(request, pk):
    task = Task.objects.get(id=pk)
    form = TaskForm(instance=task)
    if request.method == 'POST':
        task = TaskForm(request.POST, instance=task)
        if task.is_valid():
            task.save()
            return redirect('home')
    return render(request, 'main/edit.html', {'form':form})