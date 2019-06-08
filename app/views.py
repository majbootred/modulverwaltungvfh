import sys
from django.shortcuts import render, redirect
from .models import Module, Assignment, Prerequisite, Semester
from accounts.models import Student


def index_view(request):
    if request.user.is_authenticated:

        my_semesters = get_semesters(request.user)

        # liest alle zum angemeldeten User gehörenden Objekte aus dem Model Assignment,
        # in welchen eine Note eingetragen ist (für den Notenspiegel)
        all_scores = Assignment.objects.filter(score__isnull=False).filter(student__userid=request.user)

        # Notenschnitt für den Notenspiegel errechnen
        median = get_score_median(all_scores)

        return render(request, 'app/index.html',
                      {'all_scores': all_scores, 'median': median,
                       'my_semesters': my_semesters})



    # Wenn der User zwar eingeloggt ist, aber noch kein Student-Profil hat, und nicht Admin ist
    elif request.user.is_authenticated and Student.objects.filter(
            userid=request.user).count() < 0 and not request.user.is_superuser:
        return redirect('accounts:update-profile')
    else:
        return redirect('accounts:login')




# def available_models_view(request):


# Nur Test-Ansichten - vor Abgabe rausnehmen
def modulelist_view(request):
    all_entries = Module.objects.all()
    my_assignments = Assignment.objects.filter(student__userid=request.user)
    return render(request, 'app/modulelist.html', {'all_entries': all_entries, 'my_assignments': my_assignments})


def prereqlist_view(request, modul):
    prereqs = Prerequisite.objects.filter(module__MID=modul)
    return render(request, 'app/prereqlist.html', {'prereqs': prereqs, 'modul': modul})


##########

# Helper Functions

def get_semesters(user):
    my_assignments = Assignment.objects.filter(student__userid=user)
    my_semester_names = my_assignments.values_list('semester', flat=True).distinct()

    my_semesters = []

    for semester_name in my_semester_names.iterator():
        semester = Semester(semester_name)
        semester.assignments = my_assignments.filter(semester=semester.name)
        my_semesters.append(semester)

        my_semesters.sort(key=lambda r: r.start_date)

    return my_semesters


''' Schreibt das QuerySet in eine Liste, errechnet den Notendurchschnitt 
    und gibt diesen formatiert (1 Nachkommastelle) zurück
'''


def get_score_median(qs):
    scorelist = []
    median = 0.0
    for entry in qs:
        scorelist.append(entry.score)
        if len(scorelist) > 0:
            median = sum(scorelist) / len(scorelist)
    return "{:.1f}".format(median)
