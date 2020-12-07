from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import campus,examenroll,studentRegistration,studentAcademicDetails,profRegistration,course,prof_course,student_course,department
from django.contrib import messages
from django.http.response import StreamingHttpResponse
from cv2 import cv2
import numpy as np
#from .camera import VideoCamera
import dlib
from gaze_tracking import GazeTracking
from .import camera
# Create your views here.
def index(request):
    return render(request,'index.html')

def contact(request):
    return render(request,'contact.html')

def addexam(request):
    if request.method == 'POST':
        cid=request.POST['cid']
        date=request.POST['date']
        time=request.POST['starttime']
        endtime=request.POST['endtime']
        marks=request.POST['marks']
        obj=examenroll(courseId_id=cid,profId_id=request.session['pid'],marks =marks,date =date,starttime =time,endtime =endtime)
        obj.save()
        messages.info(request,"Do you want to add more exam")
        return render(request,'addexam.html')
    else:
        #data = profRegistration.objects.get(pfRegId=request.session['pid'])
        #dept = department.objects.get(deptId =data.deptId_id)
        #print(dept)
        #cid=course.objects.filter(department=dept.deptName)
        cid= prof_course.objects.all().filter(prof_id=request.session['pid']).values()        
        #cid=course.objects.filter(cid='CS111')
        stu ={
         "courseId": cid
        }
        print(stu)
        return render(request,'addexam.html',stu)
    

def exampage(request):
    return render(request,'exam.html')


def courseDetails(request):
    value = department.objects.get(deptId = request.session['dept'])
    data = course.objects.filter(department=value.deptName)
    stu = {
        "student_number": data
    }
    return render(request,"studentCourseDetails.html", stu)

def profcourseDetails(request):
    data = course.objects.filter(department=request.session['dept'])
    prof = {
        "prof_number": data
    }
    return render(request,"profcourse.html", prof)

def registration(request):
    if request.method == 'POST':
        id = request.POST['id']
        uname = request.POST['username']
        mail = request.POST['email']
        Gen = request.POST['gender']
        Birthdate = request.POST['dob']
        reg = request.POST['year']
        pic = request.POST['pic']
        pasw = request.POST['password']
        ph = request.POST['phone']
        deptid = request.POST['course']
        print(deptid)
        obj = studentAcademicDetails(sid=id,name=uname,email=mail,gender=Gen,dob=Birthdate,y_o_reg=reg,deptId_id=deptid,image=pic)
        obj.save()
        obj1 = studentRegistration(stdReg_id=id,email=mail,password=pasw,phone=ph)
        obj1.save()
        request.session['id'] = request.POST['id']
        request.session['dept'] = deptid
        return redirect(courseDetails)
        
    else:
        data = department.objects.all()
        item = {
            "itemno":data
        }
        return render(request,'registration.html',item)


def login(request):
    if request.method == 'POST':
        try:
            data =  studentRegistration.objects.get(stdReg_id=request.POST['id'])
            if data.password == request.POST['psw']:
                return render(request,'studentexam.html') 
            else:
                messages.info(request," Invalid Student Id or Password")
                return render(request,'login.html')
        except:
            messages.info(request,"Invalid Student Id or Password")
            return render(request,'login.html')
    else:
        return render(request,'login.html')


def profregistration(request):
    if request.method == 'POST':
        pid = request.POST['pid']
        pname = request.POST['username']
        mail = request.POST['email']
        deptid = department.objects.get(deptName=request.POST['course'])
        pasw = request.POST['password']
        ph = request.POST['phone']
        obj = profRegistration(pfRegId=pid,pname=pname,email=mail,deptId=deptid,password=pasw,phone=ph)
        obj.save()
        request.session['pid'] = request.POST['pid']
        request.session['dept'] = request.POST['course']
        return redirect(profcourseDetails)
    else:
        return render(request,'profReg.html')



def proflogin(request):
    if request.method == 'POST':
        try:
            data =  profRegistration.objects.get(pfRegId=request.POST['pid'])
            request.session['pid'] = request.POST['pid']
            dept = department.objects.get(deptId =data.deptId_id)
            request.session['dept'] = dept.deptName
            if data.password == request.POST['psw']:
                return render(request,'exam.html')
            else:
                messages.info(request,"Invalid Professor Id or Password")
                return render(request,'profLogin.html')
        except:
            messages.info(request,"Invalid Professor Id or Password")
            return render(request,'profLogin.html')
    else:
        return render(request,'profLogin.html')



def profcourseenroll(request):
    if request.method == 'POST':
        courseID = request.POST.getlist('cid[]')
        pid = request.session['pid']
        for x in range(len(courseID)):
           obj=  prof_course(prof_id  = pid,course_id = courseID[x])
           obj.save()
        return redirect('/')


def courseenroll(request):
    if request.method == 'POST':
        courseID = request.POST.getlist('cid[]')
        p=request.session['id']
        for x in range(len(courseID)):
            obj= student_course(student_id = p,course_id = courseID[x])
            obj.save()
        return redirect('/') 

    else:
        return redirect('/') 

def eye(request):
    if request.method == 'POST':
       return render(request,'livevideo.html')
    else:
        return render(request,'livevideo.html')

def studentvideo(request):
    if request.method == 'POST':
        return render(request,'studentvideo.html')
    else:
        return render(request,'studentvideo.html')

def video_feed(request):
     return StreamingHttpResponse(camera.gen_frames(),
					content_type='multipart/x-mixed-replace; boundary=frame')