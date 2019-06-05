from django.shortcuts import render, redirect
from .models import Module, Prerequisite, Assignment, Student

''' Schreibt das QuerySet in eine Liste, errechnet den Notendurchschnitt 
    und gibt diesen formatiert (1 Nachkommastelle) zurück
'''
def getscoremedian(qs):
    scorelist = []
    median = 0.0
    for entry in qs:
        scorelist.append(entry.score)
        if len(scorelist) > 0:
            median = sum(scorelist)/len(scorelist)
    return "{:.1f}".format(median)


def index(request):
    if request.user.is_authenticated:
        # Liest alle Objekte aus dem Model Module
        all_modules = Module.objects.all()

        # liest alle zum angemeldeten User gehörenden Objekte aus dem Model Assignment,
        # in welchen eine Note eingetragen ist (für den Notenspiegel)
        all_scores = Assignment.objects.filter(score__isnull=False).filter(student__userid=request.user)

        # Notenschnitt für den Notenspiegel errechnen
        median = getscoremedian(all_scores)

        return render(request, 'app/index.html', {'all_modules': all_modules, 'all_scores': all_scores, 'median': median})
    else:
        return redirect('accounts:login')



# Nur Test-Ansichten - vor Abgabe rausnehmen
def modulelist(request):
    all_entries = Module.objects.all()
    return render(request, 'app/modulelist.html', {'all_entries': all_entries})


def prereqlist(request, modul):
    prereqs = Prerequisite.objects.filter(module__MID=modul)
    return render(request, 'app/prereqlist.html', {'prereqs': prereqs, 'modul':modul})
