from django.shortcuts import render

from django.http import HttpResponse

# Create your views here.

def home(request):
    return render(request, 'home.html')

def demo(request):
    return render(request, 'demo.html')

def lsignup(request):
    return render(request, 'signup.html')

def lnotification(request):
    return render(request, 'notifications.html')

def lcontacts(request):
    return render(request, 'contacts.html')

def lmedia(request):
    return render(request, 'media.html')

def lhome(request):
    return render(request, 'home.html')

def lforgpasw(request):
    return render(request, 'forgpasw.html')