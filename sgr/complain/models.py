from django.db import models
from django.utils import timezone
from django.db.models import Q

from user.models import Student, Member

from datetime import datetime


class Complain(models.Model):
    id = models.CharField(max_length = 12, primary_key = True)
    subject = models.CharField(max_length = 35)
    category = models.CharField(max_length = 30)
    sub_category = models.CharField(max_length = 30)
    brief = models.TextField()
    complainer = models.ForeignKey(Student, on_delete = models.CASCADE)
    file = models.FileField(upload_to = 'complain/', blank = True, null = True)
    reg_datetime = models.DateTimeField(default = timezone.now)
    solved = models.BooleanField(default = False)
    approved = models.BooleanField(default = False)
    solver = models.ForeignKey(Member, on_delete =  models.CASCADE, blank = True, null = True)
    solve_date = models.DateField(blank = True, null = True)
    
    def get_filename(self):
        return self.file.name[9:]
    
    def search_id(query):
        return Q(id__icontains = query)

    def search_subject(query):
        return Q(subject__icontains = query)
    
    def search_category(query):
        return Q(category__icontains = query)
    
    def search_sub_category(query):
        return Q(sub_category__icontains = query)
    
    def search_brief(query):
        return Q(brief__icontains = query)
	
	
	
##class Note(models.Model):
##    note = models.TextField()
##    file = models.FileField(upload_to = 'note/', blank = True, null = True)
##    complain = models.ForeignKey(Complain, on_delete = models.CASCADE)
##    reg_datetime = models.DateTimeField(default = timezone.now)
##    solver = models.ForeignKey(Member, on_delete = models.CASCADE)