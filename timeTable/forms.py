from django import forms
from .models import *

class TimetableForm(forms.ModelForm):
    class Meta:
        model = TimeTable
        fields = ['course', 'subject', 'faculty', 'classroom', 'semester', 'day', 'time_slot']

    def __init__(self, *args, **kwargs):
        super(TimetableForm, self).__init__(*args, **kwargs)
        
        self.fields['subject'].queryset = Subject.objects.none()

        if 'course' in self.data and 'semester' in self.data:
            try:
                course_id = int(self.data.get('course'))
                semester_id = int(self.data.get('semester'))
                self.fields['subject'].queryset = Subject.objects.filter(course_id=course_id, semester_id=semester_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            course = self.instance.course
            semester = self.instance.semester
            self.fields['subject'].queryset = Subject.objects.filter(course=course, semester=semester).order_by('name')
            self.fields['subject'].initial = self.instance.subject

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'code']

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'course', 'semester']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
            'semester': forms.Select(attrs={'class': 'form-control'}),
        }