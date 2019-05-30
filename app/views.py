from django.shortcuts import render
from .models import Module


def index(request):
    all_entries = Module.objects.all()
    return render(request, 'app/index.html', {'all_entries': all_entries})
