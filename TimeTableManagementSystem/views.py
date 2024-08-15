from django.shortcuts import render, redirect
from timeTable.models import *

def index(request):
    return redirect('timetable')

def timetable(request):
    selected_course = None
    selected_semester = None
    selected_division = None

    if request.method == 'GET':
        selected_course_id = request.GET.get('course')
        selected_semester_id = request.GET.get('semester')
        selected_division = request.GET.get('division')  # Fetch selected division
        
        # Fetch selected course, semester, and division if provided
        if selected_course_id:
            selected_course = Course.objects.get(id=selected_course_id)
        if selected_semester_id:
            selected_semester = Semester.objects.get(id=selected_semester_id)
        if not selected_division:
            selected_division = 'A'  # Default to division 'A' if none is selected
    
    # Default to the first course, semester, and division if none is selected
    if not selected_course:
        selected_course = Course.objects.first()
    if not selected_semester:
        selected_semester = Semester.objects.first()
    if not selected_division:
        selected_division = 'A'

    # Retrieve timetable entries based on selected course, semester, and division
    timetable_entries = TimeTable.objects.filter(
        course=selected_course,
        semester=selected_semester,
        division=selected_division
    )
    
    days = Day.objects.all()  # Fetch all Day objects
    time_slots = [slot[0] for slot in TimeTable.TIME_SLOT_CHOICES]

    # Creating a list of dictionaries for easy access in the template
    timetable_data = []
    for time_slot in time_slots:
        row = {'time_slot': time_slot, 'entries': []}
        for day in days:
            entry = timetable_entries.filter(day=day, time_slot=time_slot).first()
            row['entries'].append(entry)
        timetable_data.append(row)

    context = {
        'timetable_data': timetable_data,
        'days': days,
        'courses': Course.objects.all(),
        'semesters': Semester.objects.all(),
        'selected_course': selected_course,
        'selected_semester': selected_semester,
        'selected_division': selected_division,
        'divisions': ['A', 'B']  # Assuming divisions are A and B
    }
    return render(request, 'timetable.html', context)
