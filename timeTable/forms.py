from django import forms
from .models import *
from django.core.exceptions import ValidationError

class TimetableForm(forms.ModelForm):
    class Meta:
        model = TimeTable
        fields = ['course', 'subject', 'faculty', 'division', 'classroom', 'semester', 'day', 'time_slot']

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

    def clean(self):
        cleaned_data = super().clean()
        faculty = cleaned_data.get('faculty')
        day = cleaned_data.get('day')
        time_slot = cleaned_data.get('time_slot')
        course = cleaned_data.get('course')
        division = cleaned_data.get('division')

        if faculty and day and time_slot and course and division:
            # Check for conflicting schedules
            conflicts = TimeTable.objects.filter(
                faculty=faculty,
                day=day,
                time_slot=time_slot
            ).exclude(id=self.instance.id)

            if conflicts.exists():
                conflict_messages = []
                for entry in conflicts:
                    conflict_messages.append(
                        f"This faculty is already scheduled at {entry.course.name} - {entry.division} division."
                    )
                raise ValidationError(" ".join(conflict_messages))


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

class FacultyForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = ['name']