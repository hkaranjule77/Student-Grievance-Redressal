from django.urls import path

from . import views

urlpatterns = [
	path( '<str:id_no>/pin/', views.pin_note, name = 'Pin Note'),
	path( '<str:id_no>/unpin/', views.unpin_note, name = 'Unpin Note'),
]
