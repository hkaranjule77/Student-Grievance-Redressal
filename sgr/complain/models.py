from django.db import models
from django.utils import timezone

from user.models import Student, Member

from datetime import datetime


class Complain(models.Model):
	id = models.CharField(max_length = 12, primary_key = True)
	subject = models.CharField(max_length = 35)
	category = models.CharField(max_length = 30)
	sub_category = models.CharField(max_length = 30)
	brief = models.TextField()
	student = models.ForeignKey(Student, on_delete = models.CASCADE)
	reg_datetime = models.DateTimeField(default = timezone.now)
	solver = models.ForeignKey(Member, on_delete =  models.CASCADE, blank = True, null = True)
	solve_date = models.DateField(blank = True, null = True)