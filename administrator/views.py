from django.shortcuts import render,HttpResponse, redirect
from .forms import MyCustomForm,TeacherForm
from .models import Class,Teacher,Teacher_Class,Student,Student_Class
from django.db.models import Count
import json
import pandas as pd
import datetime
from django.contrib import messages

def Teachers(request):
    unique_teachers = Teacher.objects.values('id','teacher_id', 'name')
    print(unique_teachers)
    return render(request,'administrator/Teachers.html',{'teachers':unique_teachers})

def Students(request):
    students = Student.objects.all().values()
    print(students)
    context = []
    for i in students:
        clas = Student_Class.objects.filter(student_id = i['id']).values()
        print(clas)
        sec = Class.objects.filter(id = clas[0]['class_id_id']).values()
        i['class'] = sec[0]["name"]
        i['section'] = sec[0]['section']
        context.append(i)
    # print(context)
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
            teacher_class_table= Teacher_Class(teacher_id= teacher, class_id= class_instance)
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
            classes_detail = Class.objects.filter(id= c.id).values()
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

def AddStudent(request,stud_id = None):

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
        if stud_id == None:
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
        else:
            student = Student.objects.get(id = stud_id)
            student.name = name
            student.email_address = email
            student.address = addr
            student.phone_no = phone
            student.gardian_or_parent_name = gard_or_par
            student.gender = gender
            student.date_of_birth = dob
            student.date_of_enrollment = enroll_date
            student.save()
            classes = Class.objects.filter(name = clas,section = section)
            print(classes)
            stud_class = Student_Class.objects.filter(student_id = stud_id)
            print(stud_class)
            for i in range(len(classes)):
                print(stud_class[i].class_id)
                print(classes[i])
                cls_updt = Student_Class.objects.get(id = stud_class[i].id )
                cls_updt.class_id = classes[i]
                cls_updt.save()
                print(stud_class[i].class_id)

            
            return redirect('administrator:Students')
               
    cls = Class.objects.values('name','section').distinct()
    cls_dict = {}
    for i in cls :
        if i['name'] not in cls_dict.keys() and i['name']!='':
            cls_dict[i['name']] = [i['section']]
        elif i['name'] in cls_dict.keys():
            cls_dict[i["name"]].append(i['section'])
    print(cls_dict)
    
    if stud_id != None:
        student = Student.objects.get(id=stud_id)
        print(student)
        stud_clas = Student_Class.objects.filter(student_id=stud_id).values()
        print(stud_clas,stud_clas[0]["id"])
        clas = Class.objects.filter(id = stud_clas[0]["class_id_id"])
        print(clas)
        cls = {}
        cls["class"] = clas[0].name
        cls["section"] = clas[0].section
        update = {"Update":True}
        return render(request,"administrator/AddStudent.html",{'class':json.dumps(cls),'student':student,'classes':json.dumps(cls_dict),'onl_classes':cls_dict.keys(),'update':json.dumps(update)})
    update = {"Update":False}
    return render(request,"administrator/AddStudent.html",{'classes':json.dumps(cls_dict),'onl_classes':cls_dict.keys(),'update':json.dumps(update)})

def DeleteStudent(request,stud_id):
    student = Student.objects.get(id = stud_id)
    student.delete()
    return redirect('administrator:Students')

def BulkAddStd(request):
    if request.method == 'POST':
        try:
            csv_file = request.FILES['csv_file']
            df = pd.read_csv(csv_file)
            dis_clasess = Class.objects.values_list("name",flat=True).distinct()
            dis_sections = Class.objects.values_list("section",flat=True).distinct()
            for index, row in df.iterrows():
                    print(row['class'],row['section'])
                    if (row["class"] in dis_clasess) or (row["section"] in dis_sections):
                        student = Student(
                        name = row['name'],email_address = row['email'],phone_no = row['phone_no'],
                        address = row['address'],gardian_or_parent_name = row['gardian_or_parent'],
                        gender = row['gender'], date_of_birth = datetime.datetime.strptime(str(row['date_of_birth']),"%d/%m/%Y").strftime("%Y-%m-%d"), 
                        date_of_enrollment = datetime.datetime.strptime(str(row['date_of_enrollment']),"%d/%m/%Y").strftime("%Y-%m-%d")
                        )
                        student.save()
                        classes = Class.objects.filter(name = row['class'],section = row['section'])
                        for i in classes:
                            stud_class = Student_Class(class_id = i,student_id = student)
                            stud_class.save()
                    else:
                        messages.warning(request,"One of the records contains class or section that is not available")
                        return redirect('administrator:AddStudent')
            messages.success(request,"Students added successfully")
            return redirect('administrator:Students')
        except:
            messages.error(request,"Failed to add students")
            return redirect('administrator:AddStudent')
    return redirect('administrator:Students')

def download_csv(request):
    # Create a DataFrame with your data
    data = {
        'name': ['Jhon'],
        'email': ['Jhon@gmail.com'],
        'phone_no': ['123456789'],
        'address': ['123 street, abc city'],
        'gardian_or_parent': ['Doe'],
        'gender': ['Male/Female/Other'],
        'date_of_birth':['18/09/2001'],
        'date_of_enrollment':['	18/08/2023'],
        'class':['1st/2nd year engineering'],
        'section':['A/B'],

        # Add more columns and data as needed
    }
    df = pd.DataFrame(data)

    # Create a response with CSV content
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data.csv"'
    df.to_csv(response, index=False)
    
    return response