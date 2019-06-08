from django.db import models
from accounts.models import Student
import datetime, sys


class Module(models.Model):
    DISCIPLINES = (
        ('MINF', 'Medieninformatik'),
        ('WINF', 'Wirtschaftsinformatik'),
    )
    MID = models.CharField(primary_key=True, max_length=5)
    Name = models.CharField(max_length=50)
    WPF = models.BooleanField(default=False)
    SS = models.BooleanField(default=True)
    WS = models.BooleanField(default=True)
    CP = models.IntegerField(default=5)
    discipline = models.CharField(max_length=4, choices=DISCIPLINES, default='MINF')


class Prerequisite(models.Model):
    DISCIPLINES = (
        ('MINF', 'Medieninformatik'),
        ('WINF', 'Wirtschaftsinformatik'),
    )
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='module')
    prereq = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='prereq')
    discipline = discipline = models.CharField(max_length=4, choices=DISCIPLINES, default='MINF')

    def __str__(self):
        return self.module.MID


class Assignment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    semester = models.CharField(max_length=7, blank=True, null=True)  # WS19/20, SS19
    accredited = models.BooleanField(default=False)
    score = models.FloatField(blank=True, null=True)


class Semester(object):
    def __init__(self, name):
        self.name = name;
        self.start_date = self.get_start_date(self.name)
        self.assignments = []

    @staticmethod
    def get_start_date(name):
        year = int("20" + name[2:4], 10)

        if name.startswith('WS'):
            month = 9
        else:
            month = 4

        return datetime.datetime(year, month, 1)
