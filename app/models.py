from django.db import models
from accounts.models import Student




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

    def __str__(self):
        return {self.MID} ({self.Name})


class Prerequisite(models.Model):
    DISCIPLINES = (
        ('MINF', 'Medieninformatik'),
        ('WINF', 'Wirtschaftsinformatik'),
    )
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='module')
    prereq = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='prereq')
    discipline = discipline = models.CharField(max_length=4, choices=DISCIPLINES, default='MINF')

    def __str__(self):
        return {self.module.MID} ({self.prereq.MID})


class Assignment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    semester = models.CharField(max_length=7, blank=True, null=True)  # WS19/20, SS19
    start_date = models.DateField(blank=True, null=True)
    accredited = models.BooleanField(default=False)
    score = models.FloatField(blank=True, null=True)

    def __str__(self):
        return {self.student.userid} ({self.module.MID})


class Semester(object):
    def __init__(self, name):
        self.name = name
        self.start_date = 0
        self.assignments = []

