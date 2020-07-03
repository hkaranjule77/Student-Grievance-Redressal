from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Permission
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType

from .models import Student, Member, questions


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
            student = Student.objects.get(sid = username)
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
            student = Student.objects.get(sid = username)
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
    if request.user.is_staff:
        try:
            member = Member.objects.get(user = request.user)
            context = { 'member' : member }
        except ObjectDoesNotExist:
            context = { 'err_msg' : 'Report in "Report Me" section about this error' }
            return render(request, 'error.html', context)
        if member.role == 'HOD' or member.role == 'Principal':
            member_list = Member.objects.all()          ### ERROR : HOD still gets list of principal user
            context.update( { 'member_list' : member_list } )
        student_list = Student.objects.all()
        context.update( { 'student_list' : student_list } )
        return render(request, 'user/list.html', context)
    return redirect('/permission-denied/')

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
		try:
			temp_user = User.objects.get(username = username)
			if not temp_user.is_active:
				context = { 'message' : 'Your account is deactivated.' +
					'Please communicate to committee member for information regarding it.'
				}
		except ObjectDoesNotExist:
			pass
		except AttributeError:
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
        student = Student.init(request)
        if student.is_valid():
            ## add verification if verified continue or redirect to register again.
            context = { 'student' : student , 'questions' : questions }
            return render(request, 'user/security-detail.html', context)
        else:
            context = { 'branches' : Student.branches, 'years' : Student.years, 'admission' : Student.admission }
            return render(request, 'user/register.html', context)
        
    context = { 'message' : 'Cannot registe when logged in. Please log out!' }
    return render(request, 'permission-denied.html', context)

def security(request):
	if not request.user.is_authenticated:
		student, valid_password = Student.init_all(request)
		if valid_password:
			password = request.POST.get('password')
			if password == request.POST.get('confirm_password'):
				student.set_security_answer(request.POST.get('security_answer'))
				student.user.save()
				student.save()
				student.user.set_password(password)
				student.user.save(update_fields = ['password'])
				context = { 'message' :
							'Account created successfully. Please login to register a complain',
							'branches' : Student.branches, 'years' : Student.years, 'admission' : Student.admission }
				return render(request, 'user/register.html', context)
			else:
				message = "Password doesn't match of both fields."
		else:
			message = 'Password is not valid. Please enter a valid password.'
		context = { 'student' : student, 'message' : message, 'questions' : questions }
		return render(request, 'user/security-detail.html', context)
	return redirct('/permission-denied/')

def profile(request, id_no):
    if request.user.is_authenticated:     
        try:
            user_obj = User.objects.get(username = id_no)
        except ObjectDoesNotExist:
            context = { 'err_msg' : 'No such user exist.' }
            return render(request, 'error.html', context)
        if user_obj.is_staff:
            try:
                member = Member.objects.get(user = user_obj)
                request_user_role = Member.objects.get(user = request.user).role
            except ObjectDoesNotExist:
                context = { 'err_msg' : 'No such Member exists.' }
                return render(request, 'error.html', context)
            if (request.user == user_obj or
                request_user_role == 'HOD' or
                request_user_role == 'Principal'):
                context = { 'member' : member }
                return render(request, 'user/mem-profile.html', context)
        else:
            if request.user.username == id_no or request.user.is_staff:
                try:
                    user = Student.objects.get(user = user_obj)
                except ObjectDoesNotExist:
                    context = { 'err_msg' : 'No such student account exists.' }
                    return render(request, 'error.html', context)
                context = { 'student' : user }
                return render(request, 'user/stu-profile.html', context)
    return redirect('/permission-denied/')

def dashboard(request):
    if request.user.is_authenticated:
        user = get_user(request.user)
        if not request.user.is_staff:
            context = { 'student' : user }
            return render(request, 'user/dashboard.html', context )
        if request.user.is_staff:
            context = {'member' : user }
            return render(request, 'user/dashboard.html', context)
    return redirect('/permission-denied/')
  
  
def deactivate(request, id_no):
	if request.user.is_staff:
		try:
			member = Member.objects.get(user = request.user)
		except ObjectDoesNotExist:
			context = { 'err_msg' : 'DEACTIVATION FAILED\n' +
				'There was some error in fetching your Member account permission.' +
				' Please report it on the website'
			}
			return render(request, 'error.html', context)
		try:
			user = User.objects.get(username = id_no)        # user to which deactivation is to addef
		except ObjectDoesNotExist:
			context = { 'err_msg' : 'No such user exist. '}
			return render(request, 'error.html', context)
		if user.is_staff:
			if member.role == 'Principal':
				try:
					deact_mem = Member.objects.get(mid = id_no)
				except ObjectDoesNotExist:
					context = { 'err_msg' : 'DEACTIVATION FAILED\n' +
						'No such Member account exist'
					}
					return render(request, 'error.html', context)
				deact_mem.deactivate(member)
				context = { 'message' : f'Member {user.username} is DEACTIVATED.'}
				return render(request, 'user/list.html', context)
		else:
			if member.role == 'HOD' or member.role == 'Principal':
				try:
					student = Student.objects.get(sid = id_no)
				except ObjectDoesNotExist:
					context = { 'err_msg' : 'DEACTIVATION FAILED\n' +
						'No such Student account exist.'
					}
					return render(request, 'error.html', context)
				student.deactivate(member)
				context = { 'message' : f'Student {user.username} is DEACTIVATED.'}
				return render(request, 'user/list.html', context)
	return render(request, 'permission-denied,html')
	
def deactivation_request(request):
	if request.user.is_staff:
		username = request.POST.get('username')
		deactivation_reason = request.POST.get('deactivation_reason')
		if deactivation_reason == '' or deactivation_reason == None:
			context = { "username" : username }
			return render(request, 'deactivation_form.html', context)
		try:
			user = User.objects.get(username = username)        # user to which deactivation is to addef
		except ObjectDoesNotExist:
			context = { 'err_msg' : 'No such user exist. '}
			return render(request, 'error.html', context)
		try:
			member = Member.objects.get(user = request.user)
		except ObjectDoesNotExist:
			context = { 'err_msg' : 
				'DEACTIVATION REQUEST CANCELLED.\n' +
				'There was some error fetching your Member account permission.' +
				' Please report it on website.' }
			return render(request, 'error.html', context)
		if user.is_staff:
			if member.role == 'HOD':
				try:
					deact_mem = Member.objects.get(user = user)
				except ObjectDoesNotExist:
					context = { 'err_msg' : 
						'DEACTIVATION REQUEST CANCELLED.\n' + 
						'No such Member account exist. Please report it on website' }
					return render(request, 'error.html', context)
				if deact_mem.deactivation_request == False:
					deact_mem.add_deactivation_request(member, deactivation_reason)
					context = { 'message' : f'Deactivation request added for {user.username}' }
					return render(request, 'user/list.html', context)
				context = { 'err_msg' : 'DEACTIVATION REQUEST CANCELLED\n' +
					'Already deactivation request  added' }
				return render(request, 'error.html', context)
		else:
			if member.role == 'Sorter':
				try:
					student = Student.objects.get(user = user)
				except ObjectDoesNotExist:
					context = { 'err_msg' : 
						'DEACTIVATION REQUEST CANCELLED.\n' + 
						'No such Student account exist. Please report it on website' }
					return render(request, 'error.html', context)
				if not student.deactivation_request:
					student.add_deactivation_request(member, deactivation_reason)
					context = { 'message' : f'Deactivation request added for {user.username}' }
					return render(request, 'user/list.html', context)
				context = { 'err_msg' : 'DEACTIVATION REQUEST CANCELLED\n' +
					'Already deactivation request  added' }
				return render(request, 'error.html', context)
	context = { 'message' : 'Please log in with proper to perform this action.'}
	return render(request, 'permission_denied.html', context)
	
def deact_request_form(request, id_no):
	if request.user.is_staff:
		try:
			user = User.objects.get(username = id_no)
		except ObjectDoesNotExist:
			context = { 'err_msg' : 'No such user exist. '}
			return render(request, 'error.html', context)
		try:
			member = Member.objects.get(user = request.user)
		except ObjectDoesNotExist:
			context = { 'err_msg' : 
								'DEACTIVATION REQUEST CANNOT BE ACCESSED\n' +
								'There was some error fetching your Member account permission.' +
								' Please report it on website.' }
			return render(request, 'error.html', context)
		if user.is_staff:
			if member.role == 'HOD':
				try:
					user = User.objects.geta(username = id_no)
				except ObjectDoesNotExist:
					context = { 'err_msg' : 
										'DEACTIVATION FAILED\n' +
										'No such user exist.'}
					return render(request, 'error.html', context)
				context = { 'username' : id_no }
				return render(request, 'user/deactivation_form.html', context)
		else:
			if member.role == 'Sorter':
				try:
					user = User.objects.get(username = id_no)
				except ObjectDoesNotExist:
					context = { 'err_msg' : 
										'DEACTIVATION FAILED\n' + 
										'No such user exists'}
					return render(request, 'error.html', context)
				context = { 'username' : id_no}
				return render(request, 'user/deactivation_form.html', context)
	return render(request, 'permission_denied.html')

def forgot_passwd(request, part):
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

def add_permission(request):
    content_type = ContentType.objects.get_for_model(Member)
    permission = Permission.objects.get(codename = Member._meta.permissions[2][0],
                                           name = Member._meta.permissions[2][1],
                                           content_type = content_type
                                           )
    return redirect('/')

def add_member(request):
    if request.user.is_staff:
        member = Member.objects.get(user = request.user)
        if member.role == 'HOD':
            member = Member()
            member.init(request)
            if member.is_non_activable():    #check whether non active account can be created.
                member.generate_mid()
                member.generate_code()    #activation code
                member.user.save()
                member.save()
                context = { 'message' : 'Member added in portal', 'roles' : Member.roles,
                            'part_2' : True, 'member' : member }
            elif member.is_non_activable_empty():
                context = { 'roles' : Member.roles }
            else:
                context = { 'message' : 'please fill out full form first', 'roles' : Member.roles }
            return render(request, 'user/add_member.html', context)
    return redirect('/permission-denied/')

def activate_member(request):
    if not request.user.is_authenticated:
        mid = request.POST.get('mid')
        context = { 'questions' : questions }
        if mid != '' and mid != None:
            try:
                member = Member.objects.get(mid = mid)
            except ObjectDoesNotExist:
                context = { 'err_msg' : 'No such user exist. Please communicate to Committee' }
                return render(request, 'error.html', context)
            if not member.activated:
                member.init_for_active(request)
                if member.is_activating_valid():
                    if member.verify_activation_code(request):
                        if request.POST.get('password') == request.POST.get('confirm_password'):
                            member.activate()                     ### saves Member
                            context.update({'message' : 'Your account is activated. Please log in to start with your work' })
                        else:
                            context.update({ 'message' : "Password in both input fields doesn't match." })
                    else:
                        context.update({ 'message' : 'Wrong Activation code. Please enter right activation code' })
                else:
                    context.update({ 'message' : 'Please fill out full form then submit it.' })
            else:
                context = { 'info_msg' : 'This accout is already activated. Please <a href = "/user/login/">login</a> here.' }
                return render(request, 'info.html', context)
        return render(request, 'user/activate_mem.html', context)
    return redirect('/permission-denied/')
