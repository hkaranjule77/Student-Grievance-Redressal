from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Student(models.Model):
	uid = models.CharField(max_length=15, primary_key=True)
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	branch = models.CharField(max_length = 25)
	year = models.CharField(max_length = 15)
	contact_no = models.CharField(max_length=15)
	reg_datetime = models.DateField(default = timezone.now)
	complain_count = models.IntegerField(blank = True, null = True)
	count_date = models.DateField(blank = True, null = True)
	
class Member(models.Model):
	mid = models.CharField(max_length = 15, primary_key = True)
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	contact_no = models.CharField(max_length=15)
	reg_datetime = models.DateField(default = timezone.now)