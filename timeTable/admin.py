from django.contrib import admin
from .models import Course, Semester, Division, Subject, AssignSubject, TimeTable, Classroom, Day


# Customize the Course admin interface
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')  # Fields to display in the list view
    search_fields = ('name', 'code')  # Fields to search in the admin interface

# Customize the Semester admin interface
class SemesterAdmin(admin.ModelAdmin):
    list_display = ['name']  # Fields to display in the list view
    search_fields = ('name',)  # Fields to search in the admin interface

# Customize the Semester admin interface
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ['name']  # Fields to display in the list view
    search_fields = ('name',)  # Fields to search in the admin interface

# Customize the Division admin interface
class DivisionAdmin(admin.ModelAdmin):
    list_display = ('name', 'course')  # Fields to display in the list view
    search_fields = ('name', 'course__name')  # Fields to search in the admin interface
    list_filter = ('course',)  # Fields to filter in the admin interface

# Customize the Subject admin interface
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'semester')  # Fields to display in the list view
    search_fields = ('name', 'division__name', 'semester__name')  # Fields to search in the admin interface
    list_filter = ('course','semester')  # Fields to filter in the admin interface

# Customize the AssignSubject admin interface
class AssignSubjectAdmin(admin.ModelAdmin):
    list_display = ('subject', 'teacher', 'semester')  # Fields to display in the list view
    search_fields = ('subject__name', 'teacher', 'semester__name')  # Fields to search in the admin interface
    list_filter = ('subject', 'semester')  # Fields to filter in the admin interface

# Customize the TimeTable admin interface
class TimeTableAdmin(admin.ModelAdmin):
    list_display = ('subject', 'day', 'start_time', 'end_time')  # Fields to display in the list view
    search_fields = ('subject__name', 'day')  # Fields to search in the admin interface
    list_filter = ('day', 'subject')  # Fields to filter in the admin interface

# Register the models with their customized admin interfaces
admin.site.register(Course, CourseAdmin)
admin.site.register(Semester, SemesterAdmin)
admin.site.register(Classroom, ClassroomAdmin)
admin.site.register(Division, DivisionAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(AssignSubject, AssignSubjectAdmin)
admin.site.register(TimeTable, TimeTableAdmin)
admin.site.register(Day)