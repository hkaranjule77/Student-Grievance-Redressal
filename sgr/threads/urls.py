from django.urls import path

from . import views

urlpatterns = [
	path('', views.list, name = 'Thread List'),
	path('<str:id_no>/', views.detail, name = 'Thread Detail'),
	path('<str:id_no>/add-note/', views.add_note, name = 'Thread Add Note'),
	path('<str:id_no>/add-redressal/',views.add_redressal, name = 'Thread Redressal'),
	path('<str:id_no>/approve/', views.approve_thread, name = 'Approve Thread'),
	path('<str:id_no>/reject-approval/', views.reject_thread, name = 'Reject Thread'),
]
