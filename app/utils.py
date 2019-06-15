from .models import Module, Assignment, Prerequisite
import sys


def get_available_modules(user, type_of_semester):
    all_modules_except_mine = get_all_modules_except_mine(user)
    all_modules_except_mine = all_modules_except_mine.filter(**{type_of_semester: True})
    available_modules_set = set()

    for module in all_modules_except_mine:
        if is_assignable(module, user):
            available_modules_set.add(module.MID)

    assignable_modules_query = Module.objects.filter(MID__in=available_modules_set)

    return assignable_modules_query


def get_all_modules_except_mine(user):
    my_assignments = Assignment.objects.filter(student__userid=user)
    my_modules = my_assignments.values('module')
    my_modules_names = list(my_modules.values_list('module_id', flat=True))
    return Module.objects.exclude(MID__in=my_modules_names)


def is_assignable(module, user, assignable=False):
    # Vorbedingungen nach übergebenem Modulkürzel filtern
    all_prerequisites = Prerequisite.objects.filter(module=module)

    # wenn leer - keine Vorbedingungen nötig - Belegung möglich
    if not all_prerequisites:
        return True
    # wenn Vorbedingungen vorhanden, Assignments nach bestandenem Modul durchsuchen
    else:
        my_assignments = Assignment.objects.filter(student__userid=user)
        # wenn der Student überhaupt schon Module belegt hat
        if my_assignments:
            # pro Vorbedingung prüfen, ob das gesuchte Modul bereits belegt wurde
            for prerequisite in all_prerequisites:
                wanted_assignments = Assignment.objects.filter(module__MID=prerequisite.prerequisite.MID,
                                                               student__userid=user)
                # wenn das vorbedingte Modul belegt wurde, prüfen ob es erfolgreich abgeschlossen wurde
                if wanted_assignments:
                    for wanted_assignment in wanted_assignments:
                        if is_passed(wanted_assignment):
                            assignable = True
                            continue
                # Modul nicht bestanden, Vorbedingung nicht erfüllt - Belegung nicht möglich
                else:
                    assignable = False
                    continue
            return assignable
        # wurde noch kein Modul belegt - Vorbedingung nicht erfüllt - Belegung nicht möglich
        else:
            return assignable


def is_passed(assignment, passed=False):
    my_score = float(assignment.score)
    if 1.0 <= my_score <= 4.0 or assignment.accredited is True:
        passed = True
    return passed
