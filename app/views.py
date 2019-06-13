import sys
from django.shortcuts import render, redirect, get_object_or_404
from .models import Module, Assignment, Prerequisite, Semester
from django.http import JsonResponse
from .forms import AssignmentForm
from accounts.models import Student
from django.http import HttpResponse
import datetime

#assignable = False

def index_view(request):
    if request.user.is_authenticated:

        my_semesters = get_semesters(request.user)

        # liest alle zum angemeldeten User gehörenden Objekte aus dem Model Assignment,
        # in welchen eine Note eingetragen ist (für den Notenspiegel)
        all_scores = Assignment.objects.filter(score__isnull=False).filter(student__userid=request.user)\
            .order_by('start_date', 'module__Name')

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


def get_modules_view(request):

    current_student = Student.objects.filter(userid=request.user)[0]

    my_assignments = Assignment.objects.filter(student__userid=current_student)
    my_modules = my_assignments.values('module')
    my_modules_names = list(my_modules.values_list('module_id', flat=True))
    all_modules_except_mine = Module.objects.exclude(MID__in=my_modules_names)

    type_of_semester = request.GET.get('type_of_semester', None)
    modules = all_modules_except_mine.filter(**{type_of_semester: True})
    return render(request, 'app/modules.html', {'modules': modules})


def get_start_date(semester):
    year = int("20" + semester[2:4], 10)

    if semester.startswith('WS'):
        month = 9
    else:
        month = 4

    return datetime.datetime(year, month, 1)

def assignment_new_view(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            current_student = Student.objects.filter(userid=request.user)[0]
            form = AssignmentForm(current_student, request.POST)
            #print(form, sys.stderr)
            if form.is_valid():
                assignment = form.save(commit=False)
                assignment.student = current_student
                assignment.semester = form.get_semester()
                assignment.module = form.get_data('module')
                assignment.accredited = form.get_data('accredited')
                assignment.score = form.get_data('score')
                assignment.start_date = get_start_date(assignment.semester)
                assignment.save()
                return redirect('app:index')
        else:
            form = AssignmentForm(user=request.user, data=request.POST)

        return render(request, 'app/assignment-new.html', {'form': form})

    else:
        return redirect('accounts:login')


def assignment_edit_view(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    if request.method == "POST":
        form = AssignmentForm(request.POST, instance=assignment)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.author = request.user
            assignment.save()
            return redirect('app:index')
    else:
        form = AssignmentForm(instance=assignment)
    return render(request, 'app/assignment-new.html', {'form': form})


# Nur Test-Ansichten - vor Abgabe rausnehmen
def modulelist_view(request):
    all_entries = Module.objects.all()

    return render(request, 'app/modulelist.html', {'all_entries': all_entries, 'my_assignments': my_assignments})


def prereqlist_view(request, my_module):
    allowed = get_prereq(my_module)
    prereqs = Prerequisite.objects.filter(module__MID=my_module)
    return render(request, 'app/prereqlist.html', {'prereqs': prereqs, 'module': my_module, 'allowed': allowed})





##########

# Helper Functions

def get_semesters(user):
    my_assignments = Assignment.objects.filter(student__userid=user)
    my_semester_names = my_assignments.values_list('semester', flat=True).distinct()

    my_semesters = []

    for semester_name in my_semester_names.iterator():
        semester = Semester(semester_name)
        semester.assignments = my_assignments.filter(semester=semester.name)
        for assignment in my_assignments:
            if assignment.semester == semester.name:
                semester.start_date = assignment.start_date
                break
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


def get_prereq(my_module, assignable=False):
    # Vorbedingungen nach übergebenem Modulkürzel filtern
    my_prereqs = Prerequisite.objects.filter(module__MID=my_module)
    # wenn leer - keine Vorbedingungen nötig - Belegung möglich
    if not my_prereqs:
        return True
    # wenn Vorbedingungen vorhanden, Assignments nach bestandenem Modul durchsuchen
    else:
        my_assignments = Assignment.objects.all()
        # wenn der Student überhaupt schon Module belegt hat
        if my_assignments:
            # pro Vorbedingung prüfen, ob das gesuchte Modul bereits belegt wurde
            for my_prereq in my_prereqs:
                wanted_assignments = Assignment.objects.filter(module__MID=my_prereq.prereq.MID)
                # wenn das vorbedingte Modul belegt wurde, prüfen ob es erfolgreich abgeschlossen wurde
                if wanted_assignments:
                    for my_assignment in wanted_assignments:
                        my_score = float(my_assignment.score)
                        if 1.0 <= my_score <= 4.0 or my_assignment.accredited == True:
                            print("Modul bestanden", file=sys.stderr)
                            #wenn erfolgreich abgeschlossen - diese eine Modulbedingung erfüllt - weitere prüfen
                            assignable=True
                            continue
                # Modul nicht bestanden, Vorbedingung nicht erfüllt - Belegung nicht möglich
                else:
                    assignable = False
                    continue
            return assignable
        # wurde noch kein Modul belegt - Vorbedingung nicht erfüllt - Belegung nicht möglich
        else:
            return False
