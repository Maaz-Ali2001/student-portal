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
    teacher=  models.ForeignKey(Teacher, on_delete=models.CASCADE)
    Class=  models.ForeignKey(Class, on_delete=models.CASCADE)
