from django import forms
from .models import TimeTable
from django.forms.widgets import TimeInput

class TimetableForm(forms.ModelForm):
    class Meta:
        model = TimeTable
        fields = ['course', 'subject', 'faculty', 'classroom', 'day', 'semester', 'start_time', 'end_time']
        widgets = {
            'start_time': TimeInput(attrs={'type': 'time'}),
            'end_time': TimeInput(attrs={'type': 'time'}),
        }