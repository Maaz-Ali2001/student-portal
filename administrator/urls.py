from django.urls import path

from . import views

app_name= 'administrator'

urlpatterns = [
    path("Teachers/", views.Teachers, name="Teachers"),
    path("Students/", views.Students, name="Students"),
    path("Classes/", views.Classes, name="Classes"),
    path("AddTeacher/", views.AddTeacher, name="AddTeacher"),
    path("AddClass/", views.AddClass, name="AddClass"),
    path("UpdateTeacher/<str:teacher_id>/", views.AddTeacher, name="UpdateTeacher"),

]