"""sgr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from . import views

urlpatterns = [
	path('', views.home, name = 'Home'),
	path('complain/', include('complain.urls'), name = 'Complain'),
	path('note/', include('complain.note_urls'), name = 'Note'),
	path('thread/', include( 'threads.urls'), name = 'Thread'),
	path('user/', include('user.urls'), name = 'User'),
	path('verification/', include('verification.urls'), name = 'Verification'),
        path('admin/', admin.site.urls),
        path('about-us/', views.about_us, name = 'About us'),
        path('contact-us/', views.contact_us, name = 'Contact us'),
        path('contact-dev/', views.contact_dev, name = 'Contact Dev'),
        path('permission-denied/', views.perm_denied, name = 'Pemission Denied'),
        path('temp/', views.temp),
        path('temp2/', views.temp2),
]

if settings.DEBUG:
	from django.conf.urls.static import static
	
	urlpatterns += static( settings.STATIC_URL, document_root = settings.STATIC_ROOT )
	
	urlpatterns += static( settings.MEDIA_URL, document_root = settings.MEDIA_ROOT )
