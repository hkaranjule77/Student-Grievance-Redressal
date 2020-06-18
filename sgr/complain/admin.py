from django.contrib import admin

from .models import Complain, Note

# Register your models here.
admin.site.register(Complain)
admin.site.register(Note)