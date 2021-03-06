from django.urls import path

from . import views

urlpatterns = [
		path('', views.list, name = 'List'),
		path('add-member/', views.add_member, name = 'Add Member'),
		path('activate-member/', views.activate_member, name = 'Activate Member'),
		path('approve/<str:id_no>/', views.approve, name = 'Approve Member'),
        path('dashboard/', views.dashboard, name = 'Dashboard'),
        path('deactivate/<str:id_no>/', views.deactivate, name = 'Deactivate'),
        path('deactivation-request/', views.deactivation_request, name = 'Deactivation Request'),
        path('deactivation-request-form/<str:id_no>/', views.deact_request_form, name = 'Deactivation Form'),
        path('forgot-passwd/', views.forgot_passwd, name = 'Forgot Password'),
        path('login/', views.log_in, name = 'Log in'),
        path('logout/', views.log_out, name = 'Log out'),
        path('profile/<str:id_no>/', views.profile, name = 'Profile'),
        path('reactivate/<str:id_no>/', views.reactivate, name = 'Reactivate'),
        path('reject-deactivation-request/<str:id_no>/', views.reject_deact_req, name = 'Reject Deactivation Request'),
        path('sign-up/', views.sign_up, name = 'Sign up'),
]
