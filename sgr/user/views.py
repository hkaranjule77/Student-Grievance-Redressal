from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.core.exceptions import ObjectDoesNotExist

from .models import Student, Member

### Not mapped ###

def get_user(user):
    '''
    NOT MAPPED IN URL
    This method take user as input and returns instance of Student/Member
    '''
    if user.is_authenticated:
        if user.is_staff:
            obj = Member.objects.get(user = user)
        else:
            obj = Student.objects.get(user = user)
        return obj
    return None


### Mapped ###


def list(request):
    return render(request, 'user/list.html')

def log_in(request):
    if not request.user.is_authenticated:
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == None and password==None:
            return render(request, 'user/login.html')
        elif username == None or password == None:
            context = {
                'message' :
                'username/password is empty. Please fill full login form and then login'
            }
            return render(reques, 'user/login.html', context)
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('/user/dashboard/')
        context = { 'message' : 'usename or passwors is wrong' }
        return render(request, 'user/login.html', context)
    return redirect('/permission-denied/')

def log_out(request):
    if request.user.is_authenticated:
        logout(request)
        return render(request, 'user/logout.html')
    return redirect('/permission-denied/')

def register(request):
    if not request.user.is_authenticated:
        branches = ( 'Chemical', 'Civil', 'Computer', 'Electrical', 'Mechanical', 'IT' )
        years = ('First', 'Second', 'Third', 'Fourth')
        admission = ( 'First year', 'Direct Second year')
        student = Student.init(request)
        if student.is_valid():
            print('valid', student.is_valid(), student.user.username)
            ### add verification if verified continue or redirect to register again.
            questions = ( 'In which town your mom/dad was born?',) 
            context = { 'student' : student , 'questions' : questions }
            return render(request, 'user/security-detail.html', context)
        else:
            context = { 'branches' : branches, 'years' : years, 'admission' : admission }
            return render(request, 'user/register.html', context)
        
    context = { 'message' : 'Cannot registe when logged in. Please log out!' }
    return render(request, 'permission-denied.html', context)

def security(request):
    if not request.user.is_authenticated:
        student, set_password = Student.init_all(request)
        if valid_password:
            password = request.POST.get('password')
            if password == request.POST.get('confirm_password'):
                student.user.set_password(password = password)
                student.user.save()
                student.save()
                return redirect('/user/dashboard/')
            else:
                message = "Password doesn't match of both fields."
        else:
            message = 'Password is not valid. Please enter a valid password.'
        context = { 'student' : student, 'message' : message }
        return render(request, 'user/security-detail.html', context)
    return redirct('/permission-denied/')

def profile(request):
    if request.user.is_authenticated:
        user = Student.objects.get(user = request.user)
        if not request.user.is_staff:
            context = { 'student' : user }
            return render(request, 'user/stu-profile.html', context)
        elif request.user.is_staff:
            context = { 'member' : user }
            return render(request, 'user/mem-profile.html', context)
    return redirect('/permission-denied/')

def dashboard(request):
    if request.user.is_authenticated:
        user = get_user(request.user)
        if not request.user.is_staff:
            context = { 'student' : user }
            return render(request, 'user/stu-dashboard.html', context )
        if request.user.is_staff:
            context = {'member' : user }
            return render(request, 'user/mem-dashboard.html', context)
    return redirect('/permission-denied/')