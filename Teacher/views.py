from django.shortcuts import render,HttpResponse, redirect
from administrator.models import Teacher,Teacher_Class,Class,Student_Class,Student
from .models import *
from .decorators import *



def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            teacher = Teacher.objects.get(teacher_id=username, password=password)
            request.session["Teacher_login"] = teacher.id
            return redirect('teacher:home')
        except Teacher.DoesNotExist:
            return HttpResponse("Authentication failed")

    return render(request,'Teacher/login.html')

def logout(request):
    pass
    # # if request.method == 'POST':

    # unique_teachers = Teacher.objects.values('id','teacher_id', 'name')
    # print(unique_teachers)
    # return render(request,'administrator/Teachers.html',{'teachers':unique_teachers})


def home(request):
    teacher_id= request.session['Teacher_login']
    all_classes=[]
    classes_id= Teacher_Class.objects.filter(teacher_id_id= teacher_id).values_list('class_id_id', flat=True)
    for c_id in classes_id:
        single_class= Class.objects.get(id= c_id)
        all_classes.append(single_class)
    print(all_classes)
    return render(request,'Teacher/home.html',context={'classes':all_classes})

def quiz_tree(request,class_name,subject,section):
    class_id= Class.objects.get(name=class_name,subject=subject,section=section)
    all_quizes= Quiz.objects.filter(class_fk=class_id)
    return render(request,'Teacher/quiz_tree.html',context={'class_name':class_name,'section':section,'subject':subject,'quizes':all_quizes})

def add_quiz(request,class_name,subject,section,quiz_id=None):
    if request.method == 'POST':
        name = request.POST['name']
        date_time = request.POST['date']
        class_id= Class.objects.get(name=class_name,subject=subject,section=section)
        students= Student_Class.objects.filter(class_id_id=class_id.id)

        if quiz_id==None:
            quiz= Quiz(name=name,date_time=date_time,class_fk=class_id)
            quiz.save()
            for stu in students:
                student_marks = request.POST[str(stu.student_id_id)]
                student_quiz= Quiz_Marks(marks=student_marks, class_student=stu,quiz_fk= quiz)
                student_quiz.save()
        else:
            quiz= Quiz.objects.get(id=quiz_id)
            quiz.name=name
            quiz.date_time= date_time
            quiz.save()
            for stu in students:
                student_marks = request.POST[str(stu.student_id_id)]
                student_quiz= Quiz_Marks.objects.get(class_student=stu,quiz_fk= quiz)
                student_quiz.marks= student_marks
                student_quiz.save()

        return redirect('teacher:quiz_tree', class_name,subject,section)

    if quiz_id==None:
        all_students=[]
        class_id= Class.objects.get(name=class_name,subject=subject,section=section)
        students= Student_Class.objects.filter(class_id_id=class_id.id)
        for stu in students:
            student= Student.objects.get(id=stu.student_id_id)            
            all_students.append(student)
            quiz=None
    else:
        all_students=[]
        class_id= Class.objects.get(name=class_name,subject=subject,section=section)
        students= Student_Class.objects.filter(class_id_id=class_id.id)
        for stu in students:
            student= Student.objects.get(id=stu.student_id_id)
            marks= Quiz_Marks.objects.get(quiz_fk_id= quiz_id,class_student_id=stu.id)
            student.marks= marks.marks
            quiz= Quiz.objects.get(id=quiz_id)
            all_students.append(student)

    return render(request,'Teacher/quiz_form.html',context={'students':all_students,'class_name':class_name,'section':section,'subject':subject,'quiz':quiz})

def attendance_tree(request,class_name,subject,section):
    class_id= Class.objects.get(name=class_name,subject=subject,section=section)
    all_attendance= Attendance.objects.filter(class_fk=class_id)
    return render(request,'Teacher/attendance_tree.html',context={'class_name':class_name,'section':section,'subject':subject,'all_attendance':all_attendance})

def add_attendance(request,class_name,subject,section,attendance_id=None):
    if request.method == 'POST':
        date_time = request.POST['date']
        class_id= Class.objects.get(name=class_name,subject=subject,section=section)
        students= Student_Class.objects.filter(class_id_id=class_id.id)

        if attendance_id==None:
            attendance= Attendance(date_time=date_time,class_fk=class_id)
            attendance.save()
            for stu in students:
                attendance_type = bool(request.POST.get(str(stu.student_id_id), False))
                # print(request.POST[str(stu.student_id_id)],stu.student_id_id)
                # return HttpResponse(attendance_type,stu.student_id_id)
                student_attendance= Attendance_student(attendance=attendance_type, class_student=stu,attendance_fk= attendance)
                student_attendance.save()
        else:
            attendance= Attendance.objects.get(id=attendance_id)
            attendance.date_time= date_time
            attendance.save()
            for stu in students:
                attendance_type = bool(request.POST.get(str(stu.student_id_id), False))
                student_attendance= Attendance_student.objects.get(class_student=stu,attendance_fk= attendance)
                student_attendance.attendance= attendance_type
                student_attendance.save()

        return redirect('teacher:attendance_tree', class_name,subject,section)

    if attendance_id==None:
        all_students=[]
        class_id= Class.objects.get(name=class_name,subject=subject,section=section)
        students= Student_Class.objects.filter(class_id_id=class_id.id)
        for stu in students:
            student= Student.objects.get(id=stu.student_id_id)            
            all_students.append(student)
            attendance=None
    else:
        all_students=[]
        class_id= Class.objects.get(name=class_name,subject=subject,section=section)
        students= Student_Class.objects.filter(class_id_id=class_id.id)
        for stu in students:
            student= Student.objects.get(id=stu.student_id_id)
            student_attendance= Attendance_student.objects.get(attendance_fk_id= attendance_id,class_student_id=stu.id)
            student.attendance= student_attendance.attendance
            attendance= Attendance.objects.get(id=attendance_id)
            all_students.append(student)

    return render(request,'Teacher/attendance_form.html',context={'students':all_students,'class_name':class_name,'section':section,'subject':subject,'attendance':attendance})

def delete_attendance(request,class_name,subject,section,attendance_id):
    Attendance_student.objects.filter(attendance_fk_id=attendance_id).delete()
    Attendance.objects.get(id = attendance_id).delete()
    return redirect('teacher:attendance_tree',class_name,subject,section)

def delete_quiz(request,class_name,subject,section,quiz_id):
    Quiz_Marks.objects.filter(quiz_fk_id=quiz_id).delete()
    Quiz.objects.get(id = quiz_id).delete()
    return redirect('teacher:quiz_tree',class_name,subject,section)