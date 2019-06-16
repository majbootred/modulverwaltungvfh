import sys
from django.shortcuts import render, redirect, get_object_or_404
from .models import Module, Assignment, Prerequisite, Semester
from django.http import JsonResponse
from .forms import AssignmentForm
from accounts.models import Student
from .utils import *
from django.http import HttpResponse
import datetime


def index_view(request):
    if request.user.is_authenticated:

        my_semesters = get_semesters(request.user)

        # liest alle zum angemeldeten User gehörenden Objekte aus dem Model Assignment,
        # in welchen eine Note eingetragen ist (für den Notenspiegel)
        all_scores = Assignment.objects.filter(score__gte=1.0, score__lte=4.0).filter(student__userid=request.user) \
            .order_by('start_date', 'module__Name')

        available_modules = get_all_modules_except_mine(request.user)
        # Notenschnitt für den Notenspiegel errechnen
        median = get_score_median(all_scores)

        return render(request, 'app/index.html',
                      {'all_scores': all_scores, 'median': median,
                       'my_semesters': my_semesters, 'available_modules': available_modules})



    # Wenn der User zwar eingeloggt ist, aber noch kein Student-Profil hat, und nicht Admin ist
    elif request.user.is_authenticated and Student.objects.filter(
            userid=request.user).count() < 0 and not request.user.is_superuser:
        return redirect('accounts:update-profile')
    else:
        return redirect('accounts:login')


def get_modules_view(request):
    current_student = Student.objects.filter(userid=request.user)[0]
    type_of_semester = request.GET.get('type_of_semester', None)
    modules = get_available_modules(current_student, type_of_semester)
    return render(request, 'app/modules.html', {'modules': modules})


def assignment_new_view(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            current_student = Student.objects.filter(userid=request.user)[0]
            form = AssignmentForm(current_student, request.POST)
            # print(form, sys.stderr)
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

        return render(request, 'app/assignment.html', {'form': form})

    else:
        return redirect('accounts:login')


def assignment_edit_view(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    if request.method == "POST":
        current_student = Student.objects.filter(userid=request.user)[0]
        form = AssignmentForm(request.POST, instance=assignment)
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
        form = AssignmentForm(instance=assignment, user=request.user)
    return render(request, 'app/assignment.html', {'form': form})


def assignment_delete_view(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    assignment.delete()
    return redirect('app:index')




# Nur Test-Ansichten - vor Abgabe rausnehmen
def modulelist_view(request):
    all_entries = Module.objects.all()

    return render(request, 'app/modulelist.html', {'all_entries': all_entries})


def prerequisites_view(request, my_module):
    allowed = is_assignable(my_module, request.user)
    prerequisites = Prerequisite.objects.filter(module__MID=my_module)
    print(allowed, sys.stderr)
    return render(request, 'app/prerequisites.html',
                  {'prerequisites': prerequisites, 'module': my_module, 'allowed': allowed})


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


def get_start_date(semester):
    year = int("20" + semester[2:4], 10)

    if semester.startswith('WS'):
        month = 9
    else:
        month = 4

    return datetime.datetime(year, month, 1)


''' Schreibt das QuerySet in eine Liste, errechnet den Notendurchschnitt 
    und gibt diesen formatiert (1 Nachkommastelle) zurück
'''


def get_score_median(all_scores):
    scores = []
    median = 0.0
    for score in all_scores:
        scores.append(score.score)
        if len(scores) > 0:
            median = sum(scores) / len(scores)
            median = str('{:.1f}'.format(median)).replace('.',',')
    return median



