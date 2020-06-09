from django.urls import path

from . import views

urlpatterns = [
	path('', views.list, name = 'List'),
        path('login/', views.log_in, name = 'Log in'),
        path('logout/', views.log_out, name = 'Log out'),
        path('register/', views.register, name = 'Register'),
        path('security-detail/', views.security, name = 'Security details'),
        path('profile/', views.profile, name = 'profile'),
        path('dashboard/', views.dashboard, name = 'dashboard'),
]