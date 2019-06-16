from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    DISCIPLINES = (
        ('MINF', 'Medieninformatik'),
        ('WINF', 'Wirtschaftsinformatik'),
    )
    userid = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, verbose_name="Benutzername")
    firstname = models.CharField(max_length=30, verbose_name="Vorname")
    lastname = models.CharField(max_length=30, verbose_name="Nachname")
    discipline = models.CharField(max_length=4, choices=DISCIPLINES, default='MINF', null=False, blank=False, verbose_name="Fachrichtung")
    startingSemester = models.CharField(max_length=7, null=False, blank=False, verbose_name="Startsemester")  # WS19/20, SS19

    def __str__(self):
        return '{}'.format(self.userid)
