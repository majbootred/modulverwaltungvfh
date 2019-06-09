from django import forms
from .models import Assignment, Module, Prerequisite
import sys


class AssignmentForm(forms.ModelForm):
    module = forms.ModelChoiceField(queryset=None)

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)

        my_assignments = Assignment.objects.filter(student__userid=user)
        my_modules = my_assignments.values('module')
        my_modules_names = list(my_modules.values_list('module_id', flat=True))
        all_modules_except_mine = Module.objects.exclude(MID__in=my_modules_names)

        # prereq = Prerequisite.objects.filter(module__MID=module)

        self.fields['module'].queryset = Module.objects.exclude(MID__in=all_modules_except_mine)

    class Meta:
        model = Assignment
        fields = ('module', 'semester', 'accredited', 'score')
