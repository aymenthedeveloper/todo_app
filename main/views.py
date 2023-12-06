from django.shortcuts import render, redirect
from .models import Task, Date
from .forms import TaskForm
from datetime import date

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

def home(request):
    q = request.GET.get('q')
    if q:
        tasks = {f'completed={q}':Task.objects.filter(completed=q)}
    else:
        dates = Date.objects.all()
        tasks = {f"{date_today}":date_today.task_set.all() for date_today in dates}
    form = TaskForm()
    if request.method == 'POST':
        task = TaskForm(request.POST)
        if task.is_valid():
            task = task.save(commit=False)
            today = Date.objects.filter(now=date.today())
            if today:
                task.date = today[0]
            else:
                task.date = Date.objects.create(now=date.today())
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