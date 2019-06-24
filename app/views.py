from django.shortcuts import render, redirect, get_object_or_404
from .forms import AssignmentForm
from accounts.models import Student
from .utils import *


def index_view(request):
    if request.user.is_authenticated:

        my_semesters = get_semesters(request.user)
        all_scores = Assignment.objects.filter(score__gte=1.0, score__lte=4.0).filter(student__userid=request.user) \
            .order_by('start_date', 'module__Name')
        available_modules = get_all_modules_except_mine(request.user)
        wpf_count = get_my_wpf_count(request.user)
        unscored_modules = get_my_unscored_modules(request.user)
        median = get_score_median(all_scores)

        return render(request, 'app/index.html',
                      {'all_scores': all_scores, 'median': median,
                       'my_semesters': my_semesters, 'available_modules': available_modules, 'wpf_count': wpf_count,
                       'unscored_modules': unscored_modules})

    # send to update profile page
    elif request.user.is_authenticated and Student.objects.filter(
            userid=request.user).count() < 0 and not request.user.is_superuser:
        return redirect('accounts:update-profile')
    # send to login page
    else:
        return redirect('accounts:login')


def assignment_new_view(request):
    if request.method == 'POST':
        current_student = Student.objects.filter(userid=request.user)[0]
        form = AssignmentForm(current_student, request.POST)
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
        form = AssignmentForm(user=request.user)

    return render(request, 'app/assignment.html', {'form': form})


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


def get_modules_view(request):
    current_student = Student.objects.filter(userid=request.user)[0]
    type_of_semester = request.GET.get('type_of_semester', None)
    year = request.GET.get('year', None)
    modules = get_available_modules(current_student, type_of_semester, int(year))
    return render(request, 'app/modules.html', {'modules': modules})


def assignment_delete_view(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    assignment.delete()
    return redirect('app:index')






