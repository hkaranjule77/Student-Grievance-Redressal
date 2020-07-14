from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Permission
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.http import HttpResponseRedirect

from .models import Student, Member, questions


### Not mapped in urls.py ###

def get_object( request, user = None, username=None):
	'''
	This method take request, user(optional), username(optional) as input and returns instance of Student/Member object.
	'''
	if username !=None:
		try:
			user = User.objects.get( username = username )
		except ObjectDoesNotExist:
			messages.error( request, f' User account with username {username} does not exist. ')
			return
	elif user == None:
		user = request.user
	if user.is_staff:
		try:
			obj = Member.objects.get(user = user)
		except ObjectDoesNotExist:
			messages.error( request, f' Member account with id {user.username} does not exist. ')
			obj = None
	elif user.is_authenticated:
		try:
			obj = Student.objects.get(user = user)
		except ObjectDoesNotExist:
			messages.error( request, f' Student account with id { user.username } does not exist. ')
			obj = None
	else:
		messages.error( request, 'Please log in to get access to different services. ')
		return None
	return obj

    ### functions required for forgot_password

def is_security_detail_valid(request):
	''' checks if forgot password form filled full. '''
	username = request.POST.get('username')
	email = request.POST.get('email')
	security_q = request.POST.get('security_question')
	answer = request.POST.get('security_answer')
	password = request.POST.get( 'password' )
	confirm_password = request.POST.get('confirm_password')
	valid = True
	if username == None:
		valid = False
	elif email == None:
		valid = False
	elif security_q == None:
		valid = False
	elif answer == None:
		valid = False
	elif password == None:
		valid = False
	elif confirm_password == None:
		valid = False
	if password != confirm_password:
		messages.error( request, "Password in both field doesn't match. ")
		valid = False
	if security_q == 'Security Question':
		messages.info( request, 'Please select Security question befor submitting.')
		valid = False
	return valid

def verify_security_details(request):
	username = request.POST.get('username')
	email = request.POST.get('email')
	security_q = request.POST.get('security_question')
	answer = request.POST.get('security_answer')
	password = request.POST.get('password')
	obj = get_object( request, username = username )			# Student / Member object
	if obj == None:
		return False
	else:
		if obj.user.email == email:
			if obj.verify_security_details(security_q, answer):
				if validate_password(password) == None:			# checks if password is valid
					obj.user.set_password( password )
					return True
				else:
					messages.error( request, 'Password is not valid. Please enter a strong password with atleast'
						+ ' 8 character long, 1 lowercase letter(a-z), 1 digit (0-9), one special symbol. ')
		else:
			messages.error( request, "Details did'nt matched with registered details. Please enter correct details. ")
			return True

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

def approve(request, id_no):
	if request.user.is_staff:
		try:
			member = Member.objects.get(user = request.user)
		except ObjectDoesNotExist:
			messages.error(request, 'Your account details doesnot exist.')
			return render(request, 'error.html')
		if member.role == 'Principal':
			try:
				approve_member = Member.objects.get(mid = id_no)
			except ObjectDoesNotExist:
				messages.error(request, f'Member account {id_no} to be approved does not exist.')
			if not approve_member.approved:
				approve_member.approve(member)
				messages.success(request, f'Member account {id_no} is approved.')
			else:
				messaged.info(request, f'Member account {id_no} is already approved.')
			return redirect( '/user/')
		messages.info(request, 'Access Denied to "approve a member". Only Principal can "approve a member".')
	return render(request, 'permission_denied.html', context)

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
		elif username == '' or password == '':
			message.info(request, 'username/password is empty. Please fill full login form and then login.' )
		user = authenticate(request, username = username, password = password)
		if user is not None:
			login(request, user)
			messages.success( request, 'Logged in successfully. ')
			if user.is_superuser:
				return redirect( '/admin/' )
			return redirect( '/user/dashboard/' )
		try:
			user = User.objects.get( username = username )
			if not user.is_active:
				messages.info( request, f' Your account { user.username } is DEACTIVATED. ')
		except ObjectDoesNotExist:
			messages.error( request, ' Wrong username and/or password. ') 
		return render( request, 'user/login.html' )
	return redirect( '/permission-denied/' )

def log_out(request):
    if request.user.is_authenticated:
        logout( request )
        messages.success( request, ' Logged out successfully. ')
        return redirect( '/user/login/')
    return redirect('/permission-denied/')
    
def reactivate(request, id_no):
	if request.user.is_staff:
		try:
			react_user = User.objects.get(username = id_no)
		except ObjectDoesNotExist:
			messages.error( request, f'No user with the id {id_no}.')
		if not react_user.is_active:
			try:
				member = Member.objects.get( user = request.user )
			except ObjectDoesNotExist:
				messages.error( request, 'Your account details does not exist.' )
			if react_user.is_staff:
				if member.role == 'Principal':
					try:
						react_mem = Member.objects.get(user = react_user)
					except ObjectDoesNotExist:
						messages.error( request, f'No Member account exist with ID { id_no }.')
					else:
						react_mem.reactivate( member )
						messages.success( request, f'Reactivated Member account with ID { id_no }')
				else:
					messages.info( 'Only Principal have access to reactivate Member accounts ')
			else:
				if member.role == 'HOD' or member.role == 'Principal':
					try:
						react_stu = Student.objects.get(user = react_user)
					except ObjectDoesNotExist:
						messages.error( request, f'No Student account exist with id {id_no}.' )
					else:
						react_stu.reactivate( member )
						messages.success( request, f'Reactivated Student account with id { id_no }')
				else:
					messages.info( 'Only HOD have access to reactivate Student accounts ')
		else:
			messages.error( request, f'User with id { id_no } is already active.')
		return redirect( '/user/' )
	return redirect('/permission-denied/')

def sign_up(request):
	if not request.user.is_authenticated:
		student, valid_password = Student.init_all(request)
		context = { 'departments' : Student.departments,
			'years' : Student.years,
			 'questions' : questions 
		}
		if student.is_valid():
			if valid_password:
				if student.password == request.POST.get('confirm_password'):
					student.final_save()							# saves final details
					messages.success( request, 'Account created successfully. Please login to register a complain.',)
				else:
					messages.info( request, "Password doesn't match of both fields.")
			else:
				messages.info( request, 'Password is not valid. Please enter a valid password.' )
		return render(request, 'user/sign_up.html', context)
	return redirct('/permission-denied/')

def profile(request, id_no):
	if request.user.is_authenticated:     
		obj = get_object( request, username = id_no )
		context = {}
		if obj == None:
			return render( request, 'error.html')
		if request.user != obj.user:
			curr_mem = get_object( request )
			context.update( { 'curr_mem' : curr_mem } )
		if obj.user.is_staff:
			if (request.user == obj.user or
				curr_mem.role == 'HOD' or
				curr_mem.role == 'Principal'):
				context.update( { 'member' : obj } )
				return render(request, 'user/mem-profile.html', context)
		else:
			if request.user.username == id_no or request.user.is_staff:
				context.update( { 'student' : obj } )
				return render(request, 'user/stu-profile.html', context)
	return redirect('/permission-denied/')

def dashboard(request):
	if request.user.is_authenticated:
		user = get_object( request )
		if user == None:
			return render( request, 'error.html')
		elif not request.user.is_staff:
			context = { 'student' : user }
			return render(request, 'user/dashboard.html', context )
		elif request.user.is_staff:
			context = {'member' : user }
			return render(request, 'user/dashboard.html', context)
	return redirect('/permission-denied/')
  
  
def deactivate(request, id_no):
	if request.user.is_staff:
		member = get_object( request )
		deact_obj = get_object( request, username = id_no )	        
		if member.role == 'Principal' or member.role == 'HOD' and not deact_obj.user.is_staff:
			if  member != deact_obj:
				if deact_obj.deactivation_request == False:
					deact_obj.deactivation_reason = request.POST.get( 'deactivation_reason' )
					if deact_obj.deactivation_reason == None or deact_obj.deactivation_reason == '':
						context = { 'username' : deact_obj.user.username }
						return render( request, 'user/deactivation_form.html', context )
					deact_obj.save( update_fields = [ 'deactivation_reason' ] )
				deact_obj.deactivate( member )
				if deact_obj.user.is_staff:
					messages.success( request, f'Member { deact_obj.user.username } is DEACTIVATED.' )
				else:
					messages.success( request, f' Student { deact_obj.user.username } is DEACTIVATED. ' )
			else:
				messages.error( request, f' You cannot deactivate your own account. ')
		else:
			messages.info( request, " You don't have proper rights to deactivate. But you can lodge a deactiavtion request. " )
		return redirect( '/user/' )
	return render(request, 'permission-denied,html')
	
def deactivation_request(request):
	if request.user.is_staff:
		username = request.POST.get('username')
		deactivation_reason = request.POST.get('deactivation_reason')
		if deactivation_reason == '' or deactivation_reason == None:
			context = { "username" : username }
			return render(request, 'deact_req_form.html', context)
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
					messages.success( request, f' Deactivation request added for {user.username}. ' )
					return render(request, 'user/list.html', context)
				messages.error( request, 'DEACTIVATION REQUEST CANCELLED\n' +
					'Already deactivation request  added' )
				return render(request, 'error.html', context)
		else:
			if member.role == 'Sorter':
				try:
					student = Student.objects.get(user = user)
				except ObjectDoesNotExist:
					messages.error( request, ' DEACTIVATION REQUEST CANCELLED.\n' + 
						'No such Student account exist. Please report it on website. ' )
					return render( request, 'error.html', context )
				if not student.deactivation_request:
					student.add_deactivation_request(member, deactivation_reason)
					messages.success( request, f'Deactivation request added for {user.username}. ' )
					return render( request, 'user/list.html', context )
				messages.error( request, 'DEACTIVATION REQUEST CANCELLED. Already deactivation request  added' )
				return render( request, 'error.html', context )
	messages.error( request, 'Please log in with proper to perform this action.' )
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
				return render(request, 'user/deact_req_form.html', context)
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
				return render(request, 'user/deact_req_form.html', context)
	return render(request, 'permission_denied.html')

def forgot_passwd(request):
	if not request.user.is_authenticated:
		context = { 'questions' : questions }
		print('hai')
		if is_security_detail_valid(request):
			print('hi')
			if verify_security_details(request):
				print('hiah')
				messages.success( request, 'Password changed successfully. ')
			else:
				print('hiafalsa')
				messages.error( request, "Details didn't matched with the registered details. ")
		#else:
		#messages.info( request,  'Please fill out full form first, then submit it.' )
		return render(request, 'user/forgot_passwd.html', context)
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
		if member.role == 'HOD' or member.role == 'Principal':
			member = Member()
			member.init( request )
			if member.is_non_activable():    #check whether non active account can be created.
				member.generate_mid()
				member.generate_code()    #activation code
				activation_code = member.activation_code
				member.set_activation_code( member.activation_code )
				member.user.save()
				member.save()
				messages.success( request, f' M  ember { member.mid } added in portal. ' )
				context = { 
					'roles' : Member.roles,
					'part_2' : True,
					'member' : member,
					'activation_code' : activation_code,
				}
			elif member.is_non_activable_empty():
				context = { 'roles' : Member.roles }
			else:
				messages.error( request, ' Please fill out full form, before submitting it. ' )
				context = { 'roles' : Member.roles }
			return render(request, 'user/add_member.html', context)
	return redirect( '/permission-denied/' )

def activate_member(request):
	''' Activates member account if approved, added in the Member model. '''
	if not request.user.is_authenticated:
		mid = request.POST.get('mid')
		context = { 'questions' : questions }
		if mid != '' and mid != None:
			try:
				member = Member.objects.get(mid = mid)
			except ObjectDoesNotExist:
				messages.error( request, 'No such user exist. Please communicate to Committee' )
				return render(request, 'error.html', context )
			if not member.activated:
				if member.approved:
					if member.user.is_active: 
						member.init_for_active(request)
						if member.is_activating_valid():
							if member.verify_activation_code(request):
								if request.POST.get('password') == request.POST.get('confirm_password'):
									member.activate()                     ### saves Member
									messages.success( request, f'Your account { mid } is activated. Now you can log in and can start with your work. ' )
								else:
									messages.error( request, "Password in both input fields doesn't match." )
							else:
								messages.error( request, 'Wrong Activation code. Please enter right activation code' )
						else:
							messages.error( request, 'Please fill out full form then submit it.' )
					else:
						messages.info(request, f'Your account { mid } has been deactivated. So you cannot activate now. ' )
				else:
					messages.info( request, 'Your is not approved yet. Please try again later or communicate to committee.' )
			else:
				messages.info( request, ' This accout is already activated. You can login, there is no need of activation. ' )
		return render(request, 'user/activate_mem.html', context)
	return redirect('/permission-denied/')
