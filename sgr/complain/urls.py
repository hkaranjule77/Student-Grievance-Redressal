from django.urls import path

from . import views

urlpatterns = [
	path('', views.list, name = 'List'),
        path('add/', views.add, name = 'Add complain'),
        path('search/', views.search, name = 'Search'),
        path('<str:id_no>/', views.detail, name = 'Detail View'),
        path('<str:id_no>/select/', views.select, name = 'Select'),
        path('<str:id_no>/deselect/', views.deselect, name = 'Deselect'),
        path('<str:id_no>/add-note/', views.add_note, name = 'Add Note'),
]