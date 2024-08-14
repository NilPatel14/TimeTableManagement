from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from timeTable import views

urlpatterns = [
    path('', views.index, name='index'),
    path('timetable',views.timetable,name="timetable"),
    path('timetable/create/', views.timetable_create, name='timetable_create'),
    path('timetable/<int:pk>/edit/', views.timetable_edit, name='timetable_edit'),
    path('timetable/<int:pk>/delete/', views.timetable_delete, name='timetable_delete'),
    path('showtimetable',views.showtimetable,name="showtimetable"),
    path('ajax/load-subjects/', views.load_subjects, name='ajax_load_subjects'),

    #--------- For Courses -----------#
    path('course-list/',views.course_list,name="course"),
    path('courses/create/', views.course_create, name='course_create'),
    path('courses/<int:pk>/edit/', views.course_edit, name='course_edit'),
    path('courses/<int:pk>/delete/', views.course_delete, name='course_delete'),
    #-----------------------------------------#

    #--------- For Courses -----------#
    path('subjects/', views.subject_list, name='subject_list'),
    path('subjects/create/', views.subject_create, name='subject_create'),
    path('subjects/<int:pk>/edit/', views.subject_edit, name='subject_edit'),
    path('subjects/<int:pk>/delete/', views.subject_delete, name='subject_delete'),
    #-----------------------------------------#
] 
