from django import forms
from .models import Assignment, Module


class AssignmentForm(forms.ModelForm):

    module = forms.ModelChoiceField(queryset=None)
    semester = forms.CharField(max_length=100)
    accredited = forms.BooleanField(widget=forms.CheckboxInput)
    score = forms.FloatField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['module'].queryset = Module.objects.all()

    class Meta:
        model = Assignment
        fields = ('module', 'semester', 'accredited', 'score')



'''

def __init__(self, user, *args, **kwargs):
        super(goForm, self).__init__(*args, **kwargs)
        self.fields['user_choice'].queryset = Document.objects.all().filter(who_upload=user)

            
            
                student = models.ForeignKey(Student, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    semester = models.CharField(max_length=7, blank=True, null=True)  # WS19/20, SS19
    accredited = models.BooleanField(default=False)
    score = models.FloatField(blank=True, null=True)
'''