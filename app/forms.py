from django import forms
from .models import Assignment, Module


class AvailableModules(forms.ModelForm):
    class Meta:
        model = Module
        fields = ('MID')

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['MID'].queryset = Module.objects.all()
