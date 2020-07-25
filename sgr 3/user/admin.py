from django.contrib import admin

from .models import Student, Member, MemberIDCount

# Register your models here.
admin.site.register(Student)
admin.site.register(Member)
admin.site.register(MemberIDCount)