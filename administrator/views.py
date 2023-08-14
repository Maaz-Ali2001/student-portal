from django.shortcuts import render,HttpResponse, redirect
from .forms import MyCustomForm,TeacherForm
from .models import Class,Teacher,Teacher_Class
from django.db.models import Count
import json

def Teachers(request):
    unique_teachers = Teacher.objects.values('id','teacher_id', 'name')
    print(unique_teachers)
    return render(request,'administrator/Teachers.html',{'teachers':unique_teachers})

def Students(request):
    return render(request,'administrator/Students.html')


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


def AddTeacher(request,teacher_id_att=None):
    if request.method == 'POST':
        name= request.POST.get('name')
        class_name= request.POST.getlist('class')
        subject= request.POST.getlist('subject')
        section= request.POST.getlist('section')
        teacher_id= request.POST.get('teacherId')
        password= request.POST.get('password')
        phone_no= request.POST.get('phoneNo')
        address= request.POST.get('address')   

        if teacher_id_att!=None:
            try:
                teacher = Teacher.objects.get(id=teacher_id_att)
                teacher.name = name
                teacher.teacher_id=teacher_id
                teacher.password=password
                teacher.address=address
                teacher.save()

                classes= Teacher_Class.objects.filter(teacher_id= teacher_id_att).delete()


            except Teacher.DoesNotExist:
                pass

        else:

            teacher= Teacher(name=name,teacher_id=teacher_id,password=password,phone_no=phone_no,address=address)
            teacher.save()

        for index in range(0,len(subject)):

            class_instance = Class.objects.get(name=class_name[index], subject=subject[index], section=section[index])
            teacher_class_table= Teacher_Class(teacher_id= teacher.id, Class_id= class_instance.id)
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

    if teacher_id_att!=None:
        classes_lst= []
        teacher = Teacher.objects.filter(id=teacher_id_att).values()
        teacher= teacher[0]
        classes = Teacher_Class.objects.filter(teacher_id=teacher['id'])
        for c in classes:
            classes_detail = Class.objects.filter(id= c.Class_id).values()
            print(classes_detail)
            classes_lst.append(classes_detail[0])
        js_classes_lst= json.dumps(classes_lst)
        teacher= json.dumps(teacher)
        return render(request, 'administrator/AddTeacher.html',{'classes':class_info_dict,'js_classes':js_classes,'js_classes_update':js_classes_lst,'js_teacher_info':teacher,'type':'update','teacherId':teacher_id_att})
    
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

