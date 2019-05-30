from django.shortcuts import render
from .models import Modules

# Create your views here.

from django.http import HttpResponse


def index(request):
    all_entries = Modules.objects.all()
    return render(request, 'app/index.html', {'all_entries': all_entries})


