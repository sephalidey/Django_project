from django.urls import path

from .import views

urlpatterns = [
    path('', views.index,name="index"),
    path('registration',views.registration,name="registration"),
    path('login',views.login,name="login"),
    path('profregistration',views.profregistration, name="profregistration"),
    path('proflogin',views.proflogin,name="proflogin"),
    path('courseenroll',views.courseenroll,name="courseenroll"),
    path('courseDetails',views.courseDetails,name="courseDetails"),
    path('contact',views.contact,name="contact"),
    path('profcourseenroll',views.profcourseenroll,name="profcourseenroll"),
    path('profcourseDetails',views.profcourseDetails,name="profcourseDetails"),
    path('exam',views.exampage,name="exam"),
    path('addexam',views.addexam,name="addexam"),
    path('eye',views.eye,name="eye"),
    #path('video',views.video,name="video"),
    path('video_feed', views.video_feed, name='video_feed'),
    path('studentvideo',views.studentvideo,name="studentvideo"),
]
