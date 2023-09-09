from django.urls import path

from . import views

app_name= 'administrator'

urlpatterns = [
    path("Teachers/", views.Teachers, name="Teachers"),
    path("Students/", views.Students, name="Students"),
    path("Classes/", views.Classes, name="Classes"),
    path("AddTeacher/", views.AddTeacher, name="AddTeacher"),
    path("AddClass/", views.AddClass, name="AddClass"),
    path("UpdateTeacher/<str:teacher_id_att>/", views.AddTeacher, name="UpdateTeacher"),
    path("AddStudent/", views.AddStudent, name="AddStudent"),
    path("UpdateStudent/<int:stud_id>", views.AddStudent, name="UpdateStudent"),
    path("DeleteStudent/<int:stud_id>",views.DeleteStudent,name="DeleteStudents"),
    path("BulkAddStd/",views.BulkAddStd,name="BulkAddStd"),
     path("DownloadSample/",views.download_csv,name="DownloadSample")
]

