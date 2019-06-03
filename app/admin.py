from django.contrib import admin
from .models import Module
from .models import Student
from .models import Prerequisite
from .models import Assignment


# Register your models here.

# admin / supercoding2019

admin.site.register(Module)
admin.site.register(Student)
admin.site.register(Prerequisite)
admin.site.register(Assignment)
