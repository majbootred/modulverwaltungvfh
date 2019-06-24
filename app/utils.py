from .models import Module, Assignment, Prerequisite, Semester
import datetime


# returns all available modules based on prerequisites and date
def get_available_modules(user, type_of_semester, year):
    all_modules_except_mine = get_all_modules_except_mine(user)
    all_modules_except_mine = all_modules_except_mine.filter(**{type_of_semester: True})
    available_modules_set = set()

    current_start_date = get_start_date(str(type_of_semester + str(year)))

    for module in all_modules_except_mine:
        if is_assignable(module, current_start_date, user):
            available_modules_set.add(module.MID)

    assignable_modules_query = Module.objects.filter(MID__in=available_modules_set)

    return assignable_modules_query


# returns all modules that are not assigned yet
def get_all_modules_except_mine(user):
    my_assignments = Assignment.objects.filter(student__userid=user)
    my_modules = my_assignments.values('module')
    my_modules_names = set(my_modules.values_list('module_id', flat=True))
    return Module.objects.exclude(MID__in=my_modules_names)


# returns whether a module has all necessary prerequisites in the passed assigned
def is_assignable(module, current_start_date, user):
    all_prerequisites = Prerequisite.objects.filter(module=module)

    if not all_prerequisites:
        return True

    else:
        my_assignments = Assignment.objects.filter(student__userid=user)

        if my_assignments:
            for prerequisite in all_prerequisites:
                necessary_assignments = Assignment.objects.filter(module__MID=prerequisite.prerequisite.MID,
                                                                  student__userid=user)
                if necessary_assignments:
                    return all_in_past(necessary_assignments, current_start_date)
                else:
                    return False
            return False
        else:
            return False


# returns whether all necessary modules are assigned in the past
def all_in_past(necessary_assignments, current_start_date):
    for necessary_assignment in necessary_assignments:
        if current_start_date > necessary_assignment.start_date:
            return True
            continue
        else:
            return False


# returns the count of all already assigned wpfs of user
def get_my_wpf_count(user):
    wpf_count = 4
    my_assignments = Assignment.objects.filter(student__userid=user)
    for assignments in my_assignments:
        if assignments.module.WPF:
            wpf_count = wpf_count - 1
    return wpf_count


# returns a list of semester objects with their assigned modules
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


# returns the start date of a semester based on semester string
def get_start_date(semester):
    year = int("20" + semester[2:4], 10)
    if semester.startswith('WS'):
        month = 9
    else:
        month = 4

    return datetime.date(year, month, 1)


# return the median of scores
def get_score_median(all_scores):
    scores = []
    median = 0.0
    for score in all_scores:
        scores.append(score.score)
        if len(scores) > 0:
            median = sum(scores) / len(scores)
            median = str('{:.1f}'.format(median)).replace('.', ',')
    return median


# returns all unscored modules of user
def get_my_unscored_modules(user):
    unscored_modules = []
    my_assignments = Assignment.objects.filter(student__userid=user)
    for assignment in my_assignments:
        if (assignment.score and assignment.score <= 4.0) or assignment.accredited:
            continue
        else:
            unscored_modules.append(assignment.module.Name + ' (' + assignment.semester + ')')
    return unscored_modules
