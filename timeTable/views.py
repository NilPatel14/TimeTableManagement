from django.shortcuts import render, get_object_or_404, redirect
from timeTable.models import *
from django.http import Http404
from .forms import TimetableForm

def index(request):
    return render(request, 'new1.html')

    
def timetable(request):
    courses = Course.objects.all()
    semesters = Semester.objects.all()

    selected_course_id = request.GET.get('course', None)
    selected_semester_id = request.GET.get('semester', None)

    filters = {}
    if selected_course_id:
        filters['subject__course_id'] = selected_course_id
    if selected_semester_id:
        filters['semester_id'] = selected_semester_id

    timetables = TimeTable.objects.filter(**filters)

    return render(request, 'index.html', {
        'timetables': timetables,
        'courses': courses,
        'semesters': semesters
    })

def timetable_create(request):
    if request.method == 'POST':
        form = TimetableForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('timetable')
    else:
        form = TimetableForm()
    return render(request, 'timetable_form.html', {'form': form})

def timetable_edit(request, pk):
    timetable = get_object_or_404(TimeTable, pk=pk)
    if request.method == 'POST':
        form = TimetableForm(request.POST, instance=timetable)
        if form.is_valid():
            form.save()
            return redirect('timetable')
    else:
        form = TimetableForm(instance=timetable)
    return render(request, 'timetable_form.html', {'form': form})

def timetable_delete(request, pk):
    timetable = get_object_or_404(TimeTable, pk=pk)
    timetable.delete()
    return redirect('timetable')
