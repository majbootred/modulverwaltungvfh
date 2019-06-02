from django.shortcuts import render, get_object_or_404
from .models import Module
from .models import Prerequisite

# Create your views here.

from django.http import HttpResponse


def index(request):
    all_entries = Module.objects.all()
    return render(request, 'app/index.html', {'all_entries': all_entries})


def modulelist(request):
    all_entries = Module.objects.all()
    return render(request, 'app/modulelist.html', {'all_entries': all_entries})


def prereqlist(request, modul):
    prereqs = Prerequisite.objects.filter(module__MID=modul)
    return render(request, 'app/prereqlist.html', {'prereqs': prereqs, 'modul':modul})
