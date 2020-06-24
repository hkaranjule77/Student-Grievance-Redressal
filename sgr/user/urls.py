from django.urls import path

from . import views

urlpatterns = [
	path('', views.list, name = 'List'),
        path('login/', views.log_in, name = 'Log in'),
        path('logout/', views.log_out, name = 'Log out'),
        path('register/', views.register, name = 'Register'),
        path('security-detail/', views.security, name = 'Security details'),
        path('profile/<str:id_no>/', views.profile, name = 'Profile'),
        path('dashboard/', views.dashboard, name = 'dashboard'),
        path('forgot-passwd/<int:part>/', views.forgot_passwd, name = 'Forgot Password'),
        path('add-member/', views.add_member, name = 'Add Member'),
        path('activate-member/', views.activate_member, name = 'Activate Member'),
]