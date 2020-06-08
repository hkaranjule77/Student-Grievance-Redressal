from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Student(models.Model):
	uid = models.CharField(max_length=15, primary_key=True)
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	branch = models.CharField(max_length = 25)
	year = models.CharField(max_length = 15)
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
            student.contact_no = request.POST.get('contact_no')
            return student
        
        def init_all(request):
            '''
            initialize student object with data from post method of request and returns student objects
            and returns boolean value of validate password
            '''
            student = Student(request)
            student.security_question = request.POST.get('security_question')
            student.security_answer = request.POST.get('security_answer')
            password = request.POST.get('password')
            if validate_password(password = password)
                return (student, False)
            else:
                return (student.True)
	
	def is_valid(self):
            valid = True
            print('uid', self.uid)
            if self.uid == '' or self.branch == '' or self.year == '' or self.contact_no == '':
                valid = False
            if self.user.username == '' or self.user.first_name == '' or self.user.last_name == '':
                valid = False
            if self.user.email == '':
                valid = False
            return valid
            
	
class Member(models.Model):
	mid = models.CharField(max_length = 15, primary_key = True)
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	contact_no = models.CharField(max_length=15)
	security_question = models.CharField(max_length = 30)
	security_answer = models.CharField(max_length = 12)
	reg_datetime = models.DateField(default = timezone.now)