from django import forms
from .utils import *
import sys


class AssignmentForm(forms.ModelForm):
    SEMESTER = [
        (u'', u'---'),
        ('WS', 'WS'),
        ('SS', 'SS')
    ]
    type_of_semester = forms.CharField(label='Sommer- oder Wintersemester',
                                       widget=forms.Select(choices=SEMESTER,
                                                           attrs={'placeholder': 'Select the category'}))
    year = forms.CharField(max_length=2, label="Jahr des Semesters (zum Beispiel 17 für WS17/18)")
    module = forms.ModelChoiceField(queryset=None, label="Modul", empty_label='---')
    score = forms.FloatField(required=False, label="Note")

    class Meta:
        model = Assignment
        fields = ('accredited',)

    def __init__(self, user, *args, **kwargs):

        super(AssignmentForm, self).__init__(*args, **kwargs)

        self.fields['module'].queryset = Module.objects.none()

        if 'type_of_semester' in self.data:
            try:
                type_of_semester = self.data.get('type_of_semester')
                assignable_modules = get_available_modules(user, type_of_semester)
                self.fields['module'].queryset = assignable_modules
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.initial['year'] = self.instance.semester[2:4]
            self.initial['type_of_semester'] = self.instance.semester[:2]
            self.initial['score'] = self.instance.score
            assignment = Assignment.objects.filter(pk=self.instance.pk)
            assignment.delete()
            self.fields['module'].queryset = get_available_modules(user, self.instance.semester[:2])
            self.fields['module'].initial = self.instance.module

    def get_semester(self):
        type_of_semester = self.cleaned_data['type_of_semester']
        year = self.cleaned_data['year']

        if type_of_semester == "WS":
            year = year + "/" + str((int(year, 10) + 1))

        return type_of_semester + year

    def get_data(self, name):
        return self.cleaned_data[name]
