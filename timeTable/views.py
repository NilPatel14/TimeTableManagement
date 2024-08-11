from django.shortcuts import render, get_object_or_404, redirect
from timeTable.models import TimeTable, User, Classroom, Subject, Course
from django.http import HttpResponse
from django.urls import reverse
from django.forms import ModelForm


# Define the TimetableForm within views.py
class TimetableForm(ModelForm):
    class Meta:
        model = TimeTable
        fields = ['subject', 'classroom', 'day', 'start_time', 'end_time']

def new(request):
    return render(request,'new1.html')
    
def index(request):
    try:
        bba_course = Course.objects.get(name='BCA')
    except Course.DoesNotExist:
        raise Http404("Course not found")
    
    timetables = TimeTable.objects.filter(
        subject__course=bba_course
    )
    return render(request, 'index.html', {'timetables': timetables})



def timetable_create(request):
    if request.method == 'POST':
        form = TimetableForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = TimetableForm()
    return render(request, 'timetable_form.html', {'form': form})

def timetable_edit(request, pk):
    timetable = get_object_or_404(TimeTable, pk=pk)
    if request.method == 'POST':
        form = TimetableForm(request.POST, instance=timetable)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = TimetableForm(instance=timetable)
    return render(request, 'timetable_form.html', {'form': form})

def timetable_delete(request, pk):
    timetable = get_object_or_404(TimeTable, pk=pk)
    timetable.delete()
    return redirect('index')
