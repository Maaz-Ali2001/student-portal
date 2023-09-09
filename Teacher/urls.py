from django.urls import path

from . import views

app_name= 'teacher'

urlpatterns = [
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("home/", views.home, name="home"),
    path("quiz/<str:class_name>/<str:subject>/<str:section>", views.quiz_tree, name="quiz_tree"),
    path("AddQuiz/<str:class_name>/<str:subject>/<str:section>", views.add_quiz, name="add_quiz"),
    path("UpdateQuiz/<str:class_name>/<str:subject>/<str:section>/<str:quiz_id>", views.add_quiz, name="update_quiz"),
    path("attendance/<str:class_name>/<str:subject>/<str:section>", views.attendance_tree, name="attendance_tree"),
    path("AddAttendance/<str:class_name>/<str:subject>/<str:section>", views.add_attendance, name="add_attendance"),
    path("UpdateAttendance/<str:class_name>/<str:subject>/<str:section>/<str:attendance_id>", views.add_attendance, name="update_attendance"),  
    path("DeleteAttendance/<str:class_name>/<str:subject>/<str:section>/<str:attendance_id>", views.delete_attendance, name="delete_attendance"),    
    path("DeleteQuiz/<str:class_name>/<str:subject>/<str:section>/<str:quiz_id>", views.delete_quiz, name="delete_quiz"),    
]