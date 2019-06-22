from django import forms
from .utils import *
import datetime, sys


class AssignmentForm(forms.ModelForm):
    SEMESTER = [
        (u'', u'---'),
        ('WS', 'WS'),
        ('SS', 'SS')
    ]
    SCORE = [
        (u'', u''),
        (1.0, '1,0'),
        (1.3, '1,3'),
        (1.7, '1,7'),
        (2.0, '2,0'),
        (2.3, '2,3'),
        (2.7, '2,7'),
        (3.0, '3,0'),
        (3.3, '3,3'),
        (3.7, '3,7'),
        (4.0, '4,0'),
        (5.0, '5,0')
    ]
    type_of_semester = forms.CharField(label='Sommer- oder Wintersemester',
                                       widget=forms.Select(choices=SEMESTER,
                                                           attrs={'placeholder': 'Select the category'}))
    year = forms.ChoiceField(choices=[(x, x+2000) for x in range(10, 30)],
                             label="Jahr des Semesters")
    module = forms.ModelChoiceField(queryset=None, label="Modul (Bitte zuerst das Semester wählen)", empty_label='---')
    score = forms.FloatField(required=False, label="Note", widget=forms.Select(choices=SCORE))

    class Meta:
        model = Assignment
        fields = ('accredited',)

    def __init__(self, user, *args, **kwargs):

        super(AssignmentForm, self).__init__(*args, **kwargs)

        self.fields['module'].queryset = Module.objects.none()
        year = get_current_year()
        print(year, sys.stderr)
        print(type(year), sys.stderr)
        self.initial['year'] = (str(year-2000), str(year))

        if self.data and 'type_of_semester' in self.data:
            try:
                type_of_semester = self.data.get('type_of_semester')
                assignable_modules = get_available_modules(user, type_of_semester, int(year))
                self.fields['module'].queryset = assignable_modules
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.initial['year'] = self.instance.semester[2:4]
            self.initial['type_of_semester'] = self.instance.semester[:2]
            self.initial['score'] = self.instance.score
            assignment = Assignment.objects.filter(pk=self.instance.pk)
            assignment.delete()
            #self.fields['module'].queryset = get_available_modules(user, self.instance.semester[:2])
            self.fields['module'].queryset = get_available_modules(user, self.instance.semester[:2], int(year))
            self.fields['module'].initial = self.instance.module

    def get_semester(self):
        type_of_semester = self.cleaned_data['type_of_semester']
        year = self.cleaned_data['year']

        if type_of_semester == "WS":
            year = year + "/" + str((int(year, 10) + 1))

        return type_of_semester + year

    def get_data(self, name):
        return self.cleaned_data[name]


def get_current_year():
    now = datetime.datetime.now()
    return now.year
