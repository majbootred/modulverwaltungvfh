from django.db import models


class Modules(models.Model):
    MID = models.CharField(max_length=4, unique=True)
    Name = models.CharField(max_length=50)
    WPF = models.BooleanField(default=0)
    SS = models.BooleanField(default=0)
    WS = models.BooleanField(default=0)
    Branch = models.CharField(max_length=4, null=True)
