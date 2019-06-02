<<<<<<< HEAD
from django.shortcuts import render, get_object_or_404
=======
from django.shortcuts import render, redirect
>>>>>>> 3e860d3a33988c3b2d1256bff5859f9f106862cd
from .models import Module
from .models import Prerequisite


def index(request):
<<<<<<< HEAD
    all_entries = Module.objects.all()
    return render(request, 'app/index.html', {'all_entries': all_entries})


def modulelist(request):
    all_entries = Module.objects.all()
    return render(request, 'app/modulelist.html', {'all_entries': all_entries})


def prereqlist(request, modul):
    prereqs = Prerequisite.objects.filter(module__MID=modul)
    return render(request, 'app/prereqlist.html', {'prereqs': prereqs, 'modul':modul})
=======
    if request.user.is_authenticated:
        all_entries = Module.objects.all()
        return render(request, 'app/index.html', {'all_entries': all_entries})
    else:
        return redirect('accounts:login')
>>>>>>> 3e860d3a33988c3b2d1256bff5859f9f106862cd
