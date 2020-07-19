from django.db import models
from django.contrib.auth.models import User
from user.models import *
# Create your models here.
class Message(models.Model):
    msg = models.TextField(null=True)
    student = models.ForeignKey(Student, null=True, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, null=True, on_delete=models.CASCADE)
    msg_flag = models.CharField(max_length=15, null=True)
    date= models.DateTimeField(auto_now=True)
