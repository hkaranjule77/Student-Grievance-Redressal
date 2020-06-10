from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone


class Student(models.Model):
	uid = models.CharField(max_length=15, primary_key=True)
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	branch = models.CharField(max_length = 25)
	year = models.CharField(max_length = 15)
	admission_type = models.CharField(max_length = 15)
	contact_no = models.CharField(max_length=15)
	security_question = models.CharField(max_length = 30)
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
            student = Student.init(request)
            student.security_question = request.POST.get('security_question')
            student.security_answer = request.POST.get('security_answer')
            password = request.POST.get('password')
            if validate_password(password = password):
                return (student, False)
            else:
                return (student, True)
	
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
            
	
class Member(models.Model):
	mid = models.CharField(max_length = 15, primary_key = True)
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	contact_no = models.CharField(max_length=15)
	security_question = models.CharField(max_length = 30)
	security_answer = models.CharField(max_length = 12)
	reg_datetime = models.DateField(default = timezone.now)