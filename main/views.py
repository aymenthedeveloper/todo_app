from django.shortcuts import render, redirect
from .models import Task, Date
from .forms import TaskForm, SignUpForm, UserEditForm
from datetime import date
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_token


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


def activate(request, uidb64, token):
    uid = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(id=uid)
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        return redirect('login_user')
    else:
        messages.error(request, "Activation link is invalid!")
        return redirect('signup_user')


def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("main/template_activate_account.html", {
        'username': user.username,
        "protocol": 'https' if request.is_secure() else 'http',
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.id)),
        'token': account_activation_token.make_token(user),
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear {user}, check your email {to_email} inbox and click on received activation link to confirm and complete the registration.\nNote: Check your spam folder.')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')


def signup_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect('home')
        else:
            messages.error(request, 'an error occured! please try again!')
            return redirect('signup_user')
    return render(request, 'main/signup_user.html', {'form': form})


# def signup_user(request):
#     form = SignUpForm()
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'you have successfully signed up!')
#             return redirect('home')
#         else:
#             messages.error(request, 'an error occured! please try again!')
#             return redirect('signup_user')
#     return render(request, 'main/signup_user.html', {'form': form})


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


@login_required(login_url='login_user')
def update_user(request):
    form = UserEditForm(instance=request.user)
    if request.method == 'POST':
        form = UserEditForm(request.POST ,instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    return render(request, 'main/edit_user.html', {'form':form})


