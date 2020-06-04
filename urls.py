from django.urls import path

from . import views

urlpatterns = [
    path('',views.home, name="home"),
    path('demo',views.demo, name="demo"),
    path('signup',views.lsignup, name="lsignup"),
    path('notifications',views.lnotification, name="lnotification"),
    path('contacts',views.lcontacts, name="lcontacts"),
    path('media',views.lmedia, name="lmedia"),
    path('home',views.lhome, name="lhome"),
    path('forgpasw',views.lforgpasw, name="lforgpasw"),


    ]
