from .models import Module, Assignment, Prerequisite, Semester
import datetime
import sys


def get_available_modules(user, type_of_semester, year):
    all_modules_except_mine = get_all_modules_except_mine(user)
    all_modules_except_mine = all_modules_except_mine.filter(**{type_of_semester: True})
    available_modules_set = set()

    actual_start_date = get_start_date(str(type_of_semester+str(year)))
    #print(actual_start_date, file=sys.stderr)

    for module in all_modules_except_mine:
        #print("Vorbedingungen suchen für "+ str(module.MID), file=sys.stderr)
        #test = is_assignable(module, actual_start_date, user)
        #print(test,file=sys.stderr)
        if is_assignable(module, actual_start_date, user):
            available_modules_set.add(module.MID)

    assignable_modules_query = Module.objects.filter(MID__in=available_modules_set)
    return assignable_modules_query


def get_all_modules_except_mine(user):
    my_assignments = Assignment.objects.filter(student__userid=user)
    my_modules = my_assignments.values('module')
    my_modules_names = list(my_modules.values_list('module_id', flat=True))
    return Module.objects.exclude(MID__in=my_modules_names)


def is_assignable(module, actual_start_date, user, assignable=False):
    # Vorbedingungen nach übergebenem Modulkürzel filtern
    all_prerequisites = Prerequisite.objects.filter(module=module)
    # wenn leer - keine Vorbedingungen nötig - Belegung möglich
    #print("Vorbedingung für " + str(module.MID), file=sys.stderr)
    if not all_prerequisites:
       #print("Keine Vorbedingungen", file=sys.stderr)
        return True
    # wenn Vorbedingungen vorhanden, Assignments nach bestandenem Modul durchsuchen
    else:
        #for a in all_prerequisites:
            #print("gesuchte Vorbedingung:")
            #print(a.prerequisite.MID)
        my_assignments = Assignment.objects.filter(student__userid=user)
        # wenn der Student überhaupt schon Module belegt hat
        if my_assignments:
            # pro Vorbedingung prüfen, ob das gesuchte Modul bereits belegt wurde
            for prerequisite in all_prerequisites:
                #print(prerequisite.prerequisite.MID, file=sys.stderr)
                wanted_assignments = Assignment.objects.filter(module__MID=prerequisite.prerequisite.MID,
                                                               student__userid=user)
                # wenn das vorbedingte Modul belegt wurde, prüfen ob es erfolgreich abgeschlossen wurde
                if wanted_assignments:
                    for wanted_assignment in wanted_assignments:
                        #print(wanted_assignment.module.MID, file=sys.stderr)
                        #print(wanted_assignment.start_date, file=sys.stderr)
                        #print(actual_start_date, file=sys.stderr)
                        #print("aktuell > belegt?", file=sys.stderr)
                        #print((actual_start_date > wanted_assignment.start_date), file=sys.stderr)
                        if actual_start_date > wanted_assignment.start_date:
                            assignable = True
                            continue
                        else:
                            assignable = False
                            return False
                # Modul nicht bestanden, Vorbedingung nicht erfüllt - Belegung nicht möglich
                else:
                    #print("Vorbedingung nicht gewählt", file=sys.stderr)
                    return False
            return assignable
        # wurde noch kein Modul belegt - Vorbedingung nicht erfüllt - Belegung nicht möglich
        else:
            return assignable


def is_passed(assignment, passed=False, my_score=0):
    if assignment.score:
        my_score = float(assignment.score)
    if assignment.accredited is True or 1.0 <= my_score <= 4.0:
        passed = True
    return passed


def get_WPF_count(user):
    wpf_count = 4
    my_assignments = Assignment.objects.filter(student__userid=user)
    for assignments in my_assignments:
        if assignments.module.WPF:
            wpf_count = wpf_count - 1
    return wpf_count


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


''' Rechnet das Startsemester in ein entsprechendes Datum um, 
um die Semester sortieren zu können
'''


def get_start_date(semester):
    year = int("20" + semester[2:4], 10)
    if semester.startswith('WS'):
        month = 9
    else:
        month = 4

    return datetime.date(year, month, 1)

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
            median = str('{:.1f}'.format(median)).replace('.', ',')
    return median


def get_unscored_modules(user):
    unscored_modules = []
    my_assignments = Assignment.objects.filter(student__userid=user)
    for assignment in my_assignments:
        if (assignment.score and assignment.score <= 4.0) or assignment.accredited:
            continue
        else:
            unscored_modules.append(assignment.module.Name + ' (' + assignment.semester + ')')
    return unscored_modules
