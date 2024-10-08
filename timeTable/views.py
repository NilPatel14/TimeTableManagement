from django.shortcuts import render, get_object_or_404, redirect
from timeTable.models import *
from django.http import Http404
from .forms import *
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test

def admin_required(user):
    return user.is_superuser

@user_passes_test(admin_required)
def index(request):
    return render(request, 'new1.html')

@user_passes_test(admin_required)
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

@user_passes_test(admin_required)
def timetable_create(request):
    course_id = request.GET.get('course')
    semester_id = request.GET.get('semester')
    division_id = request.GET.get('division')
    day_id = request.GET.get('day')
    time_slot = request.GET.get('time_slot')

    initial_data = {}
    if course_id:
        initial_data['course'] = course_id
    if semester_id:
        initial_data['semester'] = semester_id
    if division_id:
        initial_data['division'] = division_id
    if day_id:
        initial_data['day'] = day_id
    if time_slot:
        initial_data['time_slot'] = time_slot

    if request.method == 'POST':
        form = TimetableForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('showtimetable')
    else:
        form = TimetableForm(initial=initial_data)
    
    return render(request, 'timetable_form.html', {'form': form})

@user_passes_test(admin_required)
def timetable_edit(request, pk):
    timetable = get_object_or_404(TimeTable, pk=pk)
    if request.method == 'POST':
        form = TimetableForm(request.POST, instance=timetable)
        if form.is_valid():
            form.save()
            return redirect('showtimetable')
    else:
        form = TimetableForm(instance=timetable)
    return render(request, 'timetable_form.html', {'form': form})

@user_passes_test(admin_required)
def timetable_delete(request, pk):
    timetable = get_object_or_404(TimeTable, pk=pk)
    timetable.delete()
    return redirect('showtimetable')


@user_passes_test(admin_required)
def showtimetable(request):
    selected_course = None
    selected_semester = None
    selected_division = None

    if request.method == 'GET':
        selected_course_id = request.GET.get('course')
        selected_semester_id = request.GET.get('semester')
        selected_division = request.GET.get('division')  # Get the selected division
        
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
    return render(request, 'showtimetable.html', context)


@user_passes_test(admin_required)
def load_subjects(request):
    course_id = request.GET.get('course')
    semester_id = request.GET.get('semester')
    subjects = Subject.objects.filter(course_id=course_id, semester_id=semester_id)

    data = [{'id': subject.id, 'name': subject.name} for subject in subjects]
    return JsonResponse(data, safe=False)





@user_passes_test(admin_required)
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses.html', {'courses': courses})

@user_passes_test(admin_required)
def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('course')
    else:
        form = CourseForm()
    return render(request, 'course_form.html', {'form': form})

@user_passes_test(admin_required)
def course_edit(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course')
    else:
        form = CourseForm(instance=course)
    return render(request, 'course_form.html', {'form': form})

@user_passes_test(admin_required)
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    course.delete()
    return redirect('course')


@user_passes_test(admin_required)
def subject_list(request):
    course_id = request.GET.get('course')
    semester_id = request.GET.get('semester')
    
    subjects = Subject.objects.all()
    if course_id:
        subjects = subjects.filter(course_id=course_id)
    if semester_id:
        subjects = subjects.filter(semester_id=semester_id)
    
    courses = Course.objects.all()
    semesters = Semester.objects.all()

    return render(request, 'subject_list.html', {
        'subjects': subjects,
        'courses': courses,
        'semesters': semesters,
    })

@user_passes_test(admin_required)
def subject_create(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('subject_list')
    else:
        form = SubjectForm()
    return render(request, 'subject_form.html', {'form': form})

@user_passes_test(admin_required)
def subject_edit(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            return redirect('subject_list')
    else:
        form = SubjectForm(instance=subject)
    return render(request, 'subject_form.html', {'form': form})


@user_passes_test(admin_required)
def subject_delete(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        subject.delete()
        return redirect('subject_list')
    return render(request, 'subject_confirm_delete.html', {'subject': subject})

@user_passes_test(admin_required)
def faculty_list(request):
    course_id = request.GET.get('course')
    semester_id = request.GET.get('semester')
    
    faculties = Faculty.objects.all()
    if course_id:
        faculties = faculties.filter(subject__course_id=course_id).distinct()
    if semester_id:
        faculties = faculties.filter(subject__semester_id=semester_id).distinct()
    
    courses = Course.objects.all()
    semesters = Semester.objects.all()

    return render(request, 'faculty_list.html', {
        'faculties': faculties,
        'courses': courses,
        'semesters': semesters,
    })

@user_passes_test(admin_required)
def faculty_create(request):
    if request.method == 'POST':
        form = FacultyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('faculty_list')
    else:
        form = FacultyForm()
    return render(request, 'faculty_form.html', {'form': form})

@user_passes_test(admin_required)
def faculty_edit(request, pk):
    faculty = get_object_or_404(Faculty, pk=pk)
    if request.method == 'POST':
        form = FacultyForm(request.POST, instance=faculty)
        if form.is_valid():
            form.save()
            return redirect('faculty_list')
    else:
        form = FacultyForm(instance=faculty)
    return render(request, 'faculty_form.html', {'form': form})

@user_passes_test(admin_required)
def faculty_delete(request, pk):
    faculty = get_object_or_404(Faculty, pk=pk)
    faculty.delete()
    return redirect('faculty_list')