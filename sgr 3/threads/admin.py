from django.contrib import admin

from .models import Category, SubCategory, Thread

# Register your models here.
admin.site.register( Thread )
admin.site.register( Category )
admin.site.register( SubCategory )
