from django.shortcuts import render,HttpResponse, redirect
from .forms import MyCustomForm,TeacherForm
from .models import Class,Teacher,Teacher_Class,Student,Student_Class
from django.db.models import Count
import json

def Teachers(request):
    unique_teachers = Teacher.objects.values('id','teacher_id', 'name')
    print(unique_teachers)
    return render(request,'administrator/Teachers.html',{'teachers':unique_teachers})

def Students(request):
    students = Student.objects.all().values()
    context = []
    for i in students:
        clas = Student_Class.objects.filter(student_id = i['id']).values()
        sec = Class.objects.filter(id = clas[0]['class_id_id']).values()
        i['class'] = sec[0]["name"]
        i['section'] = sec[0]['section']
        context.append(i)
    print(context)
    return render(request,'administrator/Students.html',{'students':context})


def Classes(request):
    class_info = Class.objects.values('name').annotate(num_subjects=Count('subject', distinct=True),
    num_sections=Count('section', distinct=True),)

    # Access the results
    for entry in class_info:
        class_name = entry['name']
        num_subjects = entry['num_subjects']
        num_sections = entry['num_sections']
        print(f"Class Name: {class_name}, Number of Subjects: {num_subjects}, Number of Sections: {num_sections}")
    return render(request,'administrator/Classes.html',{'classes':class_info})


def AddTeacher(request,teacher_id=None):
    if request.method == 'POST':
        name= request.POST.get('name')
        class_name= request.POST.getlist('class')
        subject= request.POST.getlist('subject')
        section= request.POST.getlist('section')
        teacher_id= request.POST.get('teacherId')
        password= request.POST.get('password')
        phone_no= request.POST.get('phoneNo')
        address= request.POST.get('address')   

        newTeacher= Teacher(name=name,teacher_id=teacher_id,password=password,phone_no=phone_no,address=address)
        newTeacher.save()

        for index in range(0,len(subject)):

            class_instance = Class.objects.get(name=class_name[index], subject=subject[index], section=section[index])
            teacher_class_table= Teacher_Class(teacher_id= newTeacher, class_id= class_instance)
            teacher_class_table.save()

        return redirect('administrator:Teachers')

    unique_class_names = Class.objects.values_list('name', flat=True).distinct()
    class_info_dict = {}

    for class_name in unique_class_names:
        class_info_dict[class_name] = {
            'sections': [],
            'subjects': [],
        }

        class_info = Class.objects.filter(name=class_name)
        sections = class_info.values_list('section', flat=True).distinct()
        class_info_dict[class_name]['sections'] = list(sections)

        subjects = class_info.values_list('subject', flat=True).distinct()
        class_info_dict[class_name]['subjects'] = list(subjects)

    js_classes= json.dumps(class_info_dict)
    print(class_info_dict)

    if teacher_id!=None:
        classes_lst= []
        teacher = Teacher.objects.get(id=teacher_id) 
        classes = Teacher_Class.objects.filter(teacher_id=teacher.id)
        for c in classes:
            classes_detail = Class.objects.filter(id= c.id).values()
            classes_lst.append(classes_detail[0])
        print(classes_lst)
        js_classes_lst= json.dumps(classes_lst)
        return render(request, 'administrator/AddTeacher.html',{'classes':class_info_dict,'js_classes':js_classes,'js_classes_update':js_classes_lst})
    
    return render(request, 'administrator/AddTeacher.html',{'classes':class_info_dict,'js_classes':js_classes})

def AddClass(request):
    if request.method == 'POST':
        name= request.POST.get('ClassName')
        sections= request.POST.getlist('Section')
        subjects= request.POST.getlist('Subject')
        for sec in sections:
            for sub in subjects:
                new_class= Class(name=name,subject= sub,section=sec)
                #return HttpResponse('hi')
                new_class.save()
        return redirect('administrator:Classes')
    
    
    #all_classes= Class.objects.all()
    return render(request, 'administrator/AddClass.html')

def AddStudent(request):

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('studemail')
        phone = request.POST.get('phone_no')
        addr = request.POST.get('address')
        gard_or_par = request.POST.get('gardian_or_parent_name')
        gender = request.POST.get('gender')
        dob = request.POST.get('date_of_birth')
        enroll_date = request.POST.get('date_of_enrollment')
        clas = request.POST.get('class')
        section = request.POST.get('section')
        student = Student(
            name = name,email_address = email,phone_no = phone,
            address = addr,gardian_or_parent_name = gard_or_par,
            gender = gender, date_of_birth = dob, 
            date_of_enrollment = enroll_date
            )
        student.save()
        classes = Class.objects.filter(name = clas,section = section)
        for i in classes:
            stud_class = Student_Class(class_id = i,student_id = student)
            stud_class.save()
        return redirect('administrator:Students')
    cls = Class.objects.values('name','section').distinct()
    cls_dict = {}
    for i in cls :
        if i['name'] not in cls_dict.keys() and i['name']!='':
            cls_dict[i['name']] = [i['section']]
        elif i['name'] in cls_dict.keys():
            cls_dict[i["name"]].append(i['section'])
    print(cls_dict)
    return render(request,"administrator/AddStudent.html",{'classes':json.dumps(cls_dict),'onl_classes':cls_dict.keys()})

