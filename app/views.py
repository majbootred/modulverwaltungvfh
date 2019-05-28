from django.shortcuts import render
from .models import Module

# Create your views here.

from django.http import HttpResponse


def index(request):
    all_entries = Module.objects.all()
    return render(request, 'app/db_inhalt.html', {'all_entries': all_entries})


