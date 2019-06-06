from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Student(models.Model):
    DISCIPLINES = (
        ('MINF', 'Medieninformatik'),
        ('WINF', 'Wirtschaftsinformatik'),
    )
    userid = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    discipline = models.CharField(max_length=4, choices=DISCIPLINES, default='MINF')
    startingSemester = models.CharField(max_length=7)  # WS19/20, SS19
