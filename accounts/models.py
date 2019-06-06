from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


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

    '''
    @receiver(post_save, sender=User)
    def create_user_student(sender, instance, created, **kwargs):
        if created:
            Student.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_student(sender, instance, **kwargs):
        instance.student.save()
    '''


'''
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
'''
