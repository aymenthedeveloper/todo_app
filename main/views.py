from django.shortcuts import render, redirect
from .models import Task, Date
from .forms import TaskForm, SignUpForm
from datetime import date
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View


def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
            username = request.POST.get('username').lower()
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'an error occured! please try again!')
                return redirect('login_user')
    return render(request, 'main/login.html', {})

def signup_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'you have successfully signed up!')
            return redirect('home')
        else:
            messages.error(request, 'an error occured! please try again!')
            return redirect('signup_user')
    return render(request, 'main/signup_user.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('login_user')


class Home(View):
    template_name = 'main/index_copy.html'
    def get(self, request):
        if request.user.is_authenticated:
            q = request.GET.get('q')
            current_user = request.user
            dates = Date.objects.filter(user=current_user)
            if q:
                tasks = {date:date.task_set.filter(completed=q) for date in dates}
            else:
                tasks = {date:date.task_set.all() for date in dates}
            form = TaskForm()
            context = {'tasks': tasks, 'form':form}
            return render(request, 'main/index_copy.html', context)
        else:
            return redirect('login_user')
    def post(self, request):
        task = TaskForm(request.POST)
        current_user = request.user
        dates = Date.objects.filter(user=current_user)
        if task.is_valid():
            task = task.save(commit=False)
            today, created = Date.objects.get_or_create(user=current_user, now=date.today())
            task.user = current_user
            task.date = today
            task.save()
            [d.delete() for d in dates if not d.task_set.all()]
            return redirect('home')
        context = {'form':task}
        return render(request, 'main/index_copy.html', context)


@login_required(login_url='login_user')
def home(request):
    q = request.GET.get('q')
    current_user = request.user
    dates = Date.objects.filter(user=current_user)
    if q:
        tasks = {date:date.task_set.filter(completed=q) for date in dates}
    else:
        tasks = {date:date.task_set.all() for date in dates}
    form = TaskForm()
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            today, created = Date.objects.get_or_create(user=current_user, now=date.today())
            form.user = current_user
            form.date = today
            form.save()
            [d.delete() for d in dates if not d.task_set.all()]
            return redirect('home')
    context = {'tasks': tasks, 'form':form}
    return render(request, 'main/index_copy.html', context)


@login_required(login_url='login_user')
def user_profile(request):
    user = request.user
    context = {'user':user}
    return render(request, 'main/user_profile.html', context)


@login_required(login_url='login_user')
def delete_task(request, pk):
    task = Task.objects.get(id=pk)
    task.delete()
    return redirect('home')


@login_required(login_url='login_user')
def complete_task(request, pk):
    task = Task.objects.get(id=pk)
    task.completed = not task.completed
    task.save()
    return redirect('home')


@login_required(login_url='login_user')
def edit_task(request, pk):
    task = Task.objects.get(id=pk)
    form = TaskForm(instance=task)
    if request.method == 'POST':
        task = TaskForm(request.POST, instance=task)
        if task.is_valid():
            task.save()
            return redirect('home')
    return render(request, 'main/edit.html', {'form':form})