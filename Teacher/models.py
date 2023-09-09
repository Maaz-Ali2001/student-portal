from django.db import models
from administrator.models import Student_Class,Class

class Quiz(models.Model):
    name = models.CharField(max_length=100)
    date_time = models.DateTimeField()
    class_fk = models.ForeignKey(Class,on_delete=models.CASCADE)


    def __str__(self):
        return self.date_time
    
class Quiz_Marks(models.Model):
    class_student = models.ForeignKey(Student_Class,on_delete=models.CASCADE)
    quiz_fk = models.ForeignKey(Quiz,on_delete=models.CASCADE)
    marks = models.FloatField()


    def __str__(self):
        return self.marks
    

class Attendance(models.Model):
    date_time = models.DateTimeField()
    class_fk = models.ForeignKey(Class,on_delete=models.CASCADE)

    def __str__(self):
        return self.date_time
    
class Attendance_student(models.Model):
    class_student = models.ForeignKey(Student_Class,on_delete=models.CASCADE)
    attendance_fk = models.ForeignKey(Attendance,on_delete=models.CASCADE)
    attendance = models.BooleanField(default=False)


    def __str__(self):
        return self.attendance