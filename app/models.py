from django.db import models
from accounts.models import Student


class Module(models.Model):
    DISCIPLINES = (
        ('MINF', 'Medieninformatik'),
        ('WINF', 'Wirtschaftsinformatik'),
    )
    MID = models.CharField(primary_key=True, max_length=5, verbose_name="Modul-ID")
    Name = models.CharField(max_length=50, verbose_name="Modul-Name")
    WPF = models.BooleanField(default=False)
    SS = models.BooleanField(default=True)
    WS = models.BooleanField(default=True)
    CP = models.IntegerField(default=5)
    discipline = models.CharField(max_length=4, choices=DISCIPLINES, default='MINF', verbose_name="Fachrichtung")

    def __str__(self):
        return '{} ({})'.format(self.MID, self.Name)


class Prerequisite(models.Model):
    DISCIPLINES = (
        ('MINF', 'Medieninformatik'),
        ('WINF', 'Wirtschaftsinformatik'),
    )
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='module', verbose_name="Modul-ID")
    prerequisite = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='prereq', verbose_name="Vorbedingung")
    discipline = discipline = models.CharField(max_length=4, choices=DISCIPLINES, default='MINF', verbose_name="Fachrichtung")

    def __str__(self):
        return '{} ({})'.format(self.module.MID, self.prerequisite.MID)


class Assignment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Benutzername")
    module = models.ForeignKey(Module, on_delete=models.CASCADE, verbose_name="Modul-ID")
    semester = models.CharField(max_length=7, blank=True, null=True, verbose_name="Semester")  # WS19/20, SS19
    start_date = models.DateField(blank=True, null=True)
    accredited = models.BooleanField(default=False, verbose_name="anerkannt")
    score = models.FloatField(blank=True, null=True, verbose_name="Note")

    def __str__(self):
        return '{} ({})'.format(self.student.userid, self.module.MID)


class Semester(object):
    def __init__(self, name):
        self.name = name
        self.start_date = 0
        self.assignments = []
