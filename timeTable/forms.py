from django import forms
from .models import *

class TimetableForm(forms.ModelForm):
    class Meta:
        model = TimeTable
        fields = ['course', 'subject', 'faculty', 'classroom', 'day', 'semester', 'time_slot']
