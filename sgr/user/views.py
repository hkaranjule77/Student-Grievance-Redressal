from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ObjectDoesNotExist

from .models import Student, Member

### GLOBAL_VAR ###

branches = ( 'Chemical', 'Civil', 'Computer', 'Electrical', 'Mechanical', 'IT' )
years = ('First', 'Second', 'Third', 'Fourth')
admission = ( 'First year', 'Direct Second year')
questions = ( 'In which town your mom/dad was born?',
              'What is name of your grand mother/grand father?',
              'What was your childhood nickname?',
              'which sports do you like most?',) 

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

    ### forgot_passwd

def is_security_detail_valid(request):
    user_type = request.POST.get('user_type')
    username = request.POST.get('username')
    security_q = request.POST.get('security_question')
    answer = request.POST.get('answer')
    valid = True
    if user_type == '' or user_type == None:
        valid = False
    elif username == '' or username == None:
        valid = False
    elif security_q == '' or security_q == None:
        valid = False
    elif answer == '' or answer == None:
        valid = False
    return valid

def verify_security_details(request):
    user_type = request.POST.get('user_type')
    username = request.POST.get('username')
    security_q = request.POST.get('security_question')
    answer = request.POST.get('answer')
    if user_type == 'student':
        try:
            student = Student.objects.get(uid = username)
        except ObjectDoesNotExist:
            return False
        else:
            return student.verify_security_details(security_q, answer)
    elif user_type == 'member':
        try:
            member = Member.objects.get(mid = username)
        except ObjectDoesNotExist:
            return False
        else:
            return member.verify_security_details(security_q, answer)
    else:
        return False

def is_password_valid(request):
    password = request.POST.get('password')
    c_password = request.POST.get('confirm_password')
    valid = False
    if password == '' or password == None:
        valid = None
    elif c_password == '' or c_password == None:
        valid = None
    elif password == c_password:
        valid = True
    return valid

def set_password(request):
    user_type = request.POST.get('user_type')
    username = request.POST.get('username')
    password = request.POST.get('password')
    if user_type == 'student':
        try:
            student = Student.objects.get(uid = username)
            user = student.user
        except ObjectDoesNotExist:
            pass
    elif user_type == 'member':
        try:
            member = Member.object.get(mid = username)
            user = member.user
        except ObjectDoesNotExist:
            pass
    if validate_password(password) == None:
        user.set_password(password)
        user.save( update_fields = ['password'] )
    
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
        global branches
        global years
        global admission
        global questions
        student = Student.init(request)
        if student.is_valid():
            ## add verification if verified continue or redirect to register again.
            context = { 'student' : student , 'questions' : questions }
            return render(request, 'user/security-detail.html', context)
        else:
            context = { 'branches' : branches, 'years' : years, 'admission' : admission }
            return render(request, 'user/register.html', context)
        
    context = { 'message' : 'Cannot registe when logged in. Please log out!' }
    return render(request, 'permission-denied.html', context)

def security(request):
    if not request.user.is_authenticated:
        student, valid_password = Student.init_all(request)
        if valid_password:
            password = request.POST.get('password')
            if password == request.POST.get('confirm_password'):
                student.user.save()
                student.save()
                student.user.set_password(password)
                student.user.save(update_fields = ['password'])
                context = { 'message' :
                            'Account created successfully. Please login to register a complain',
                            'branches' : branches, 'years' : years, 'admission' : admission }
                return render(request, 'user/register.html', context)
            else:
                message = "Password doesn't match of both fields."
        else:
            message = 'Password is not valid. Please enter a valid password.'
        global questions
        context = { 'student' : student, 'message' : message, 'questions' : questions }
        return render(request, 'user/security-detail.html', context)
    return redirct('/permission-denied/')

def profile(request):
    if request.user.is_authenticated:     
        if request.user.is_staff:
            user = Member.objects.get(user = request.user)
            context = { 'member' : user }
            return render(request, 'user/mem-profile.html', context)
        else:
            user = Student.objects.get(user = request.user)
            context = { 'student' : user }
            return render(request, 'user/stu-profile.html', context)
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

def forgot_passwd(request, part):
    global questions
    if not request.user.is_authenticated:
        if part == 0:                             ### PART_0 - render a blank form
            context = { 'part' : 0,
                        'questions' : questions}
            return render(request, 'user/forgot_passwd.html', context)
        elif part == 1:                            ### PART_1 - verify details and render password form
            if is_security_detail_valid(request):
                if verify_security_details(request):
                    context = { 'part' : 1, 'user_type' : request.POST.get('user_type'),
                                'username' : request.POST.get('username') }
                else:
                    context = { 'part' : 0, 'message' : 'please enter correct details',
                                'questions' : questions}
            else:
                context = { 'part' : 0,
                            'message' : 'Please fill out full form first, then submit it.',
                            'questions' : questions,}
            return render(request, 'user/forgot_passwd.html', context)
        elif part == 2:
            valid = is_password_valid(request)
            context = { 'user_type' : request.POST.get('user_type'),
                        'username' : request.POST.get('username') }
            if valid:
                set_password(request)
                context.update( { 'part' : 2 } )
            elif valid == None:             ### if any password field is empty
                context.update( { 'part' : 1,
                                  'message' : 'Please fill out full form first, then submit it' } )
            else:                           ### if password in both field deosn't match
                context.update( { 'part' : 1,
                                  'message' : "Password in both field doesn't match." } )
            return render(request, 'user/forgot_passwd.html', context)
        else:
            context = { 'err_msg' : '404 : Page not found' }
            return render(request, 'error.html', context)
    return redirect('/permission-denied/')