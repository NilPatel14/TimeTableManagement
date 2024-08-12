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
    path('showtimetable',views.showtimetable,name="showtimetable")
] 
