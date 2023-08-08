from django.shortcuts import render,HttpResponse, redirect
from .forms import MyCustomForm,TeacherForm
from .models import Class,Teacher
from django.db.models import Count
import json

def Teachers(request):
    return render(request,'administrator/Teachers.html')

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


def AddTeacher(request):
    if request.method == 'POST':
        name= request.POST.get('name')
        class_name= request.POST.get('class')
        subject= request.POST.get('subject')
        section= request.POST.get('section')
        teacher_id= request.POST.get('teacherId')
        password= request.POST.get('password')
        phone_no= request.POST.get('phoneNo')
        address= request.POST.get('address')   

        class_instance = Class.objects.get(name=class_name, subject=subject, section=section)
        classId = class_instance.id
        newClass= Teacher(name=name,teacher_id=teacher_id,password=password,phone_no=phone_no,address=address,class_taught=classId)
        newClass.save()


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

