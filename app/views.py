from django.shortcuts import render, redirect
from .models import Module
from .models import Prerequisite


def index(request):
    if request.user.is_authenticated:
        all_entries = Module.objects.all()
        return render(request, 'app/index.html', {'all_entries': all_entries})
    else:
        return redirect('accounts:login')


def modulelist(request):
    all_entries = Module.objects.all()
    return render(request, 'app/modulelist.html', {'all_entries': all_entries})


def prereqlist(request, modul):
    prereqs = Prerequisite.objects.filter(module__MID=modul)
    return render(request, 'app/prereqlist.html', {'prereqs': prereqs, 'modul':modul})
