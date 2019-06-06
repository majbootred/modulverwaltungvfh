from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout,authenticate
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .forms import StudentForm
from django.http import HttpResponse


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if user.is_superuser:
                return redirect('app:index')
            else:
                return redirect('accounts:update-profile')
    else:
        form = UserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('app:index')
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('app:index')


@login_required
@transaction.atomic
def update_student_view(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        current_user = request.user
        if form.is_valid():
            student = form.save(commit=False)
            student.userid = current_user
            student.save()
            return redirect('app:index')
        else:
            return HttpResponse('This page shows a list of most recent posts.')
    else:
        form = StudentForm()
    return render(request, 'accounts/update-profile.html', {'form': form})
