from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone

import random
from datetime import date

questions = (( '1', 'In which town your mom/dad was born?'),
             ( '2', 'What is name of your grand mother/grand father?'),
             ( '3', 'What was your childhood nickname?'),
             ( '4', 'which sports do you like most?',)
             )

class Student(models.Model):
    
    ### CONSTANTS
    
    branches = ( ('chemical', 'Chemical'),
                 ('civil','Civil'),
                 ('computer', 'Computer'),
                 ('electrical', 'Electrical'),
                 ('mechanical', 'Mechanical'),
                 ('it', 'IT' ),
                 )
    years = (('1st', 'First'),
             ('2nd', 'Second'),
             ('3rd', 'Third'),
             ('4th', 'Fourth'),
             )
    admission = (('FH', 'First year'),
                 ('DS', 'Direct Second year'))
    global questions
    
    ### MODELS
    
    uid = models.CharField(max_length=15, primary_key=True)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    branch = models.CharField(max_length = 12)
    year = models.CharField(max_length = 10)
    admission_type = models.CharField(max_length = 12)
    contact_no = models.CharField(max_length=15)
    security_question = models.CharField(max_length = 40)
    security_answer = models.CharField(max_length = 12)
    reg_datetime = models.DateField(default = timezone.now)
    complain_count = models.IntegerField(blank = True, null = True)
    count_date = models.DateField(blank = True, null = True)
    
    
    def init(request):
        user = User()
        user.username = request.POST.get('uid')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        student = Student(user = user)
        student.uid = user.username
        student.branch = request.POST.get('branch')
        student.year = request.POST.get('year')
        student.admission_type = request.POST.get('admission_type')
        student.contact_no = request.POST.get('contact_no')
        return student
    
    def init_all(request):
        '''
        initialize the student object with data from post method of request and returns
        tuple of student and boolean value of validate_password.
        '''
        global questions
        student = Student.init(request)
        for code, question in questions:
            if request.POST.get('security_question') == question:
                student.security_question = (code, question)
        student.security_answer = request.POST.get('security_answer')
        password = request.POST.get('password')
        if validate_password(password) == None:
            return (student, True)
        else:
            return (student, False)
    
    def is_valid(self):
        valid = True
        if  self.uid == '' or self.uid == None:
            valid = False
        if  self.branch == '' or self.branch == None:
            valid = False
        if self.year == '' or self.year == None:
            valid = False
        if self.admission_type == '' or self.admission_type == None:
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
        return valid
    
    def verify_security_details(self, security_q, answer):
        if self.security_question == security_q and self.security_answer == answer:
            return True
        else:
            return False


class MemberIDCount (models.Model):
    next_solver_id = models.IntegerField()
    next_sorter_id = models.IntegerField()
    next_db_admin_id = models.IntegerField()
    next_hod_id = models.IntegerField()

class Member(models.Model):
    ### CONTSTANTS
    
    roles = (('L', 'Solver'),
             ('R', 'Sorter'),
             ('D', 'DB Admin'),
             ('H', 'HOD')
             )
    global questions
    
    mid = models.CharField(max_length = 15, primary_key = True)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    role = models.CharField(max_length = 15)
    contact_no = models.CharField(max_length=15)
    security_question = models.CharField(max_length = 40)
    security_answer = models.CharField(max_length = 12)
    reg_datetime = models.DateField(default = timezone.now)
    activated = models.BooleanField(default = False)
    activation_code = models.CharField(max_length = 8)
    activated_datetime = models.DateTimeField(default = timezone.now, null = True, blank = True)
        
    def verify_security_details(self, security_q, answer):
        if self.security_question == security_q and self.security_answer == answer:
            return True
        else:
            return False
        
    def init(self, request):
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
        self.security_question = request.POST.get('security_question')
        self.security_answer = request.POST.get('answer')
        password = request.POST.get('password')
        if validate_password(password = password) == None:
            self.user.set_password(password)
    
    ### methods for creating non active account
    
    def is_non_activable(self):
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
            print(5)
        return empty
    
    def generate_mid(self):
        curr_date = date.today()
        curr_year = curr_date.strftime('%y')
        count_obj = MemberIDCount.objects.first()
        if self.role == 'HOD':
            next_id = count_obj.next_hod_id
            count_obj.next_hod_id += 1
        elif self.role == 'DB Admin':
            next_id = count_obj.next_db_admin_id
            count_obj.next_db_admin_id += 1
        elif self.role == 'Sorter':
            next_id = count_obj.next_sorter_id
            count_obj.next_sorter_id += 1
        elif self.role == 'Solver':
            next_id = count_obj.next_solver_id
            count_obj.next_solver_id += 1
        id = str(next_id) 
        id_len = len(id)
        for index in range(len(Member.roles)):
            if self.role == Member.roles[index][1]:
                role_code = Member.roles[index][0]
        for count in range(3-id_len):
            id = '0' + id
        mid = curr_year + role_code + id
        self.mid = mid
        self.user.username = mid
        count_obj.save( update_fields = ['next_solver_id',
                                         'next_sorter_id',
                                         'next_db_admin_id',
                                         'next_hod_id'] )
    
    #generates activaton code
    def generate_code(self):
        code = ''
        for count in range(8):
            code += str(random.randint(0,9))
        self.activation_code = code
        
    ### FOR ACTIVATING THE ACCOUNT
        
    def verify_activation_code(self, request):
        if self.activation_code == request.POST.get('activation_code'):
            return True
        return False
    
    def is_activating_valid(self):
        if self.security_answer == '' or self.security_answer == None:
            return False
        return True
        
    def activate(self):
        self.activated = True
        self.save(update_fields = [ 'security_question',
                                    'security_answer',
                                    'activated',
                                    'activated_datetime'])