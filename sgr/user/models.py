from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

import random
from datetime import date, datetime

questions = ('In which town your mom/dad was born?',
				'What is name of your grand mother?',
				'What was your childhood nickname?',
				'Which sports do you like most?',
             )
             
             
             
class MemberIDCount (models.Model):
    next_solver_id = models.IntegerField()
    next_sorter_id = models.IntegerField()
    next_db_admin_id = models.IntegerField()
    next_hod_id = models.IntegerField()
    next_principal_id = models.IntegerField()
    count_date = models.DateField(default = timezone.now)
        
    def initialize():
        ''' For initializing new object, if no object is present. '''
        id_count_obj = MemberIDCount()
        id_count_obj.next_solver_id = 0
        id_count_obj.next_sorter_id = 0
        id_count_obj.next_db_admin_id = 0
        id_count_obj.next_hod_id = 0
        id_count_obj.next_principal_id = 0
        id_count_obj.count_date = date.today()
        id_count_obj.save(update_fields = ['next_solver_id',
                                           'next_sorter_id',
                                           'next_hod_id',
                                           'next_principal_id',
                                           'count_date', ])
        return id_count_obj
    
    def reinitialize():
        ''' If new year starts, call this function to initialize all value to zero. '''
        try:
            id_count_obj = MemberIDCount.objects.first()
        except ObjectDoesNotExist:
            id_count_obj = MemberIDCount()
        id_count_obj.next_solver_id = 0
        id_count_obj.next_sorter_id = 0
        id_count_obj.next_db_admin_id = 0
        id_count_obj.next_hod_id = 0
        id_count_obj.next_principal_id = 0
        id_count_obj.count_date = date.today()
        id_count_obj.save(update_fields = ['next_solver_id',
                                           'next_sorter_id',
                                           'next_hod_id',
                                           'next_principal_id',
                                           'count_date', ])
    


class Member(models.Model):
	mid = models.CharField(max_length = 15, primary_key = True)
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	role = models.CharField(max_length = 15)
	contact_no = models.CharField(max_length=15)
	security_question = models.CharField(max_length = 40)
	security_answer = models.CharField(max_length = 100)
	reg_datetime = models.DateField(default = timezone.now)
	# Activation of account
	activated = models.BooleanField(default = False)
	activation_code = models.CharField(max_length = 8)
	activated_datetime = models.DateTimeField(default = timezone.now, null = True, blank = True)
	# Approval of account
	approved = models.BooleanField( default = False )
	approved_by = models.ForeignKey(
		'self',
		related_name = 'member approved by member+',
		on_delete = models.SET_NULL,
		null = True,
		blank = True
	)
	approved_at = models.DateTimeField(null = True, blank = True)
	# Reactivation
	reactivated_by = models.ForeignKey( 
		'self',
		related_name = 'reactivated by member+',
		on_delete = models.SET_NULL,
		null = True,
		blank = True
	)
	reativated_at = models.DateTimeField( null = True, blank = True )
	# Deactivation request
	deactivation_request = models.BooleanField(default = False)
	deact_requested_mem = models.ForeignKey(
		'self',
		on_delete = models.SET_NULL,
		null = True,
		blank = True
	)
	deactivation_reason = models.TextField(null = True, blank = True)
	deact_req_at = models.DateTimeField(null = True, blank = True)
	# Deactivation
	deactivated_by = models.ForeignKey(
		'self',
		related_name = 'member_deactivated_by',
		on_delete = models.SET_NULL, 
		null = True,
		blank = True
	)
	deactivated_at = models.DateTimeField(null = True, blank = True)
	  ### CONTSTANTS

	roles = (('L', 'Solver'),
			 ('R', 'Sorter'),
			 ('D', 'DB Admin'),
			 ('H', 'HOD'),
			 ('P', 'Principal'),
			 )
	global questions

		
	def init(self, request):
		''' Assigns data from form to object for creating a non_active account. '''
		user = User()
		user.first_name = request.POST.get('first_name')
		user.last_name = request.POST.get('last_name')
		user.email = request.POST.get('email')
		user.is_staff = True
		self.user = user
		self.role = request.POST.get('role')
		self.contact_no = request.POST.get('contact_no')
		self.activation_code = request.POST.get('activation_code')
		
	def init_for_active(self, request):
		''' Assigns data from form to object for activation of account. '''
		self.security_question = request.POST.get('security_question')
		self.security_answer = request.POST.get('answer')
		password = request.POST.get('password')
		print(request.POST.get('password'))
		if validate_password(password = password) == None:
			self.user.set_password(password)

	def is_non_activable(self):
		''' Checks data assigned to object is not empty string('')/None, while creating new account '''
		valid = True
		if self.user.first_name == '' or self.user.first_name == None:
			valid = False
		elif self.user.last_name == '' or self.user.last_name == None:
			valid = False
		elif self.user.email == '' or self.user.email == None:
			valid = False
		elif self.role == '' or self.role == None:
			valid = False
		elif self.contact_no == '' or self.contact_no == None:
			valid = False
		return valid

	def is_non_activable_empty(self):
		''' Checks data assigned to object is not empty string('')/None, while activating new account '''
		empty = True
		if self.user.first_name != '' and self.user.first_name != None:
			empty = False
		elif self.user.last_name != '' and self.user.last_name != None:
			empty = False
		elif self.user.email != '' and self.user.email != None:
			empty = False
		elif self.role != '' and self.role != None:
			empty = False
		elif self.contact_no != '' and self.contact_no != None:
			empty = False
		return empty

	def generate_mid(self):
		''' Generates Member ID while creation of account. '''
		curr_date = date.today()
		curr_year = curr_date.strftime('%y')
		try:
			count_obj = MemberIDCount.objects.first()
		except ObjectDoesNotExist:
			count_obj = MemberIDCount.initialize()
		# If year changes, reinitialize the Count
		if curr_year != count_obj.count_date.strftime('%y'):
			count_obj = MemberIDCount.reinitialze()
		# Getting role_code and count of roles of member
		if self.role == 'HOD':
			next_id = count_obj.next_hod_id
			count_obj.next_hod_id += 1
			role_code = 'H'
		elif self.role == 'DB Admin':
			next_id = count_obj.next_db_admin_id
			count_obj.next_db_admin_id += 1
			role_code = 'D'
		elif self.role == 'Sorter':
			next_id = count_obj.next_sorter_id
			count_obj.next_sorter_id += 1
			role_code = 'R'
		elif self.role == 'Solver':
			next_id = count_obj.next_solver_id
			count_obj.next_solver_id += 1
			role_code = 'L'
		elif self.role == 'Principal':
			next_id = count_obj.next_principal_id
			count_obj.next_principal_id += 1
			role_code = 'P'
		count_obj.save( update_fields = ['next_solver_id',
										 'next_sorter_id',
										 'next_db_admin_id',
										 'next_hod_id',
										 'next_principal_id'] )
		id = str(next_id) 
		id_len = len(id)
		for count in range(3-id_len):
			id = '0' + id
		mid = curr_year + role_code + id   # final addition of mid 
		self.mid = mid                     # mid assigned to object
		self.user.username = mid 
		
	# generates activaton code 
	def generate_code(self):
		''' Generates random ACTIVATION CODE. '''
		code = ''
		for count in range(8):
			code += str(random.randint(0,9))
		self.activation_code = code
		
	def approve(self, member):
		''' Approves added Member account in models. '''
		self.approved = True
		self.approved_by = member
		self.approved_at = timezone.now()
		self.save( update_fields = [
				'approved',
				'approved_at',
				'approved_by',
			]
		)

	# verifies activation code
	def verify_activation_code(self, request):
		''' Verifies 8 digit ACTIVATION CODE '''
		if self.activation_code == request.POST.get('activation_code'):
			return True
		return False

	def verify_security_details(self, security_q, answer):
		''' Verifies security question for forgot password feature'''
		if (self.security_question == security_q and check_password(answer, self.security_answer)):
			return True
		else:
			return False

	def is_activating_valid(self):
		''' Validates data at time of activation of account. '''
		if self.security_answer == '' or self.security_answer == None:
			return False
		return True
		
	def activate(self):
		self.activated = True
		self.user.save(update_fields = ['password'])
		self.save(update_fields = [ 
									'security_question',
									'security_answer',
									'activated',
									'activated_datetime']
		)

	def set_security_answer(self, answer):
		self.security_answer = make_password(answer)
		
	def reactivate( self, member ):
		''' Make changes in model for reactivation. '''
		self.user.is_active = True
		self.user.save( update_fields = [ 'is_active' ] )
		self.deactivation_request = False
		self.reactivated_by = member
		self.reactivated_at = timezone.now()
		self.save( update_fields = [
				'deactivation_request',
				'reactivated_by',
				'reactivated_at',
			]
		)
		
	def add_deactivation_request(self, member, deactivation_reason):
		''' Adds and save deactivation request details in model '''
		self.deactivation_request = True
		self.deact_requested_mem = member
		self.deactivation_reason = deactivation_reason
		self.deact_req_at = datetime.now()
		self.save( update_fields = [
				'deactivation_request',
				'deact_requested_mem',
				'deactivation_reason',
				'deact_req_at',] 
		)
		
	def deactivate(self, member):
		''' Deactivates member account. '''
		self.user.is_active = False
		self.deactivated_by = member
		self.deactivated_at = datetime.now()
		self.user.save( update_fields = [ 'is_active' ] )
		self.save( update_fields = [ 'deactivated_by', 'deactivated_at' ] )
	
			 

class Student(models.Model):
	# registration detail
	sid = models.CharField(max_length=15, primary_key=True)
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	department = models.CharField(max_length = 12)
	year = models.CharField(max_length = 10)
	contact_no = models.CharField(max_length=15)
	reg_datetime = models.DateField(default = timezone.now)
	# security details
	security_question = models.CharField(max_length = 40)
	security_answer = models.CharField(max_length = 100)
	# for limiting the complain registration
	complain_count = models.IntegerField(blank = True, null = True)
	count_date = models.DateField(blank = True, null = True)
	# Reactivation
	reactivated_by = models.ForeignKey( 
		Member,
		related_name = 'student reactivated by member+',
		on_delete = models.SET_NULL,
		null = True,
		blank = True
	)
	reactivated_at = models.DateTimeField( null = True, blank = True )
	# Deactivation request
	deactivation_request = models.BooleanField(default = False)
	deact_requested_mem = models.ForeignKey(
		Member,
		related_name = 'deactivation_requested_member',
		on_delete = models.SET_NULL,
		null = True,
		blank = True
	)
	deactivation_reason = models.TextField(null = True, blank = True)
	deact_req_at = models.DateTimeField(null = True, blank = True)
	# Deactivation
	deactivated_by = models.ForeignKey(
		Member,
		related_name = 'account_deactivated_by',
		on_delete = models.SET_NULL,
		null = True, 
		blank = True
	)
	deactivated_at = models.DateTimeField( null = True, blank = True)
	
	### CONSTANTS
	departments = ( 'Chemical',
				 'Civil',
				 'Computer',
				 'Electrical',
				 'Mechanical',
				 'IT',
	)
	years = ('First',
					'Second',
					'Third',
					'Fourth',
	)
	global questions

	def init(request):
		''' Initialize a student object with form data. '''
		user = User()
		user.username = request.POST.get('sid')
		user.first_name = request.POST.get('first_name')
		user.last_name = request.POST.get('last_name')
		user.email = request.POST.get('email')
		student = Student(user = user)
		student.sid = user.username
		student.department = request.POST.get('department')
		student.year = request.POST.get('year')
		student.contact_no = request.POST.get('contact_no')
		return student

	def init_all(request):
		'''
		initialize the student object with data from post method of request and returns
		tuple of student and boolean value of validate_password.
		'''
		global questions
		student = Student.init(request)
		for question in questions:
			if request.POST.get('security_question') == question:
				student.security_question = question
		student.security_answer = request.POST.get('security_answer')
		password = request.POST.get('password')
		student.password = password
		if password is not None:
			if validate_password(password) == None:
				return (student, True)
		return (student, False)

	def is_valid(self):
		valid = True
		if  self.sid == '' or self.sid == None:
			valid = False
		if  self.department == '' or self.department == None:
			valid = False
		if self.year == '' or self.year == None:
			valid = False
		if  self.contact_no == '' or self.contact_no == None:
			valid = False
		if self.user.username == '' or self.user.username == None:
			valid = False
		if self.user.first_name == '' or self.user.first_name == None:
			valid = False
		if self.user.last_name == '' or self.user.last_name == None:
			valid = False
		if self.user.email == '' or self.user.email == None:
			valid = False
		if self.security_question == '' or self.security_question == None:
			valid = False
		if self.security_answer == '' or self.security_answer == None:
			valid = False
		return valid
		
	def set_security_answer(self, answer):
		self.security_answer = make_password(answer)
		
	def final_save( self):
		self.set_security_answer( self.security_answer )
		self.user.set_password( self.password )
		self.user.save()
		self.save()

	def verify_security_details(self, security_q, answer):
		''' Verifies security question for forgot password feature'''
		if (self.security_question == security_q and check_password(answer, self.security_answer)):
			return True
		else:
			return False
		
	def reactivate( self, member ):
		''' Make changes in model for reactivation. '''
		self.user.is_active = True
		self.user.save( update_fields = [ 'is_active' ] )
		self.deactivation_request = False
		self.reactivated_by = member
		self.reactivated_at = timezone.now()
		self.save( update_fields = [
				'deactivation_request',
				'reactivated_by',
				'reactivated_at',
			]
		)
		
	def add_deactivation_request(self, member, deactivation_reason):
		''' Adds and save deactivation request details in model '''
		self.deactivation_request = True
		self.deact_requested_mem = member
		self.deactivation_reason = deactivation_reason
		self.deact_req_at = datetime.now()
		self.save( update_fields = [
				'deactivation_request',
				'deact_requested_mem',
				'deactivation_reason',
				'deact_req_at',] 
		)
	
	def deactivate(self, member):
		''' Deactivates member account. '''
		self.user.is_active = False
		self.deactivated_by = member
		self.deactivated_at = datetime.now()
		self.user.save( update_fields = [ 'is_active' ] )
		self.save( update_fields = [ 'deactivated_by', 'deactivated_at' ] )
				


