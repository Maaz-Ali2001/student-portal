from django.db import models

class Class(models.Model):
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    section = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    teacher_id = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=100)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Teacher_Class(models.Model):
    teacher_id=  models.ForeignKey(Teacher, on_delete=models.CASCADE)
    class_id=  models.ForeignKey(Class, on_delete=models.CASCADE)


class Student(models.Model):
    name = models.CharField(max_length=100)
    email_address = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=100)
    address = models.CharField(max_length=250)
    gardian_or_parent_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    date_of_enrollment = models.DateField()

    def __str__(self):
        return self.name

class Student_Class(models.Model):
    class_id = models.ForeignKey(Class,on_delete=models.CASCADE)
    student_id = models.ForeignKey(Student,on_delete=models.CASCADE)

    