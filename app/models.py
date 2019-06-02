from django.db import models

class Module(models.Model):
    DISCIPLINES = (
        ('MINF', 'Medieninformatik'),
        ('WINF', 'Wirtschaftsinformatik'),
    )
    MID = models.CharField(primary_key=True, max_length=5)
    Name = models.CharField(max_length=50)
    WPF = models.BooleanField(default=0)
    SS = models.BooleanField(default=0)
    WS = models.BooleanField(default=0)
    CP = models.IntegerField(default=5)
    discipline = models.CharField(max_length=4, choices=DISCIPLINES, default='MINF')


class Prerequisite(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='module')
    prereq = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='prereq')

    def __str__(self):
        return self.module.MID

class Student(models.Model):
    DISCIPLINES = (
        ('MINF', 'Medieninformatik'),
        ('WINF', 'Wirtschaftsinformatik'),
    )
    userid = models.EmailField(primary_key=True)
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    branch = models.CharField(max_length=4, choices=DISCIPLINES, default='MINF')
    startingSemester = models.CharField(max_length=7)


class Completed(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    accredited = models.BooleanField(default=0)
    score = models.FloatField()
