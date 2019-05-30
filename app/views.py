from django.shortcuts import render, redirect
from .models import Module


def index(request):
    if request.user.is_authenticated:
        all_entries = Module.objects.all()
        return render(request, 'app/index.html', {'all_entries': all_entries})
    else:
        return redirect('accounts:login')
