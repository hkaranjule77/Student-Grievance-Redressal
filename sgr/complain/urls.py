from django.urls import path

from . import views

urlpatterns = [
		path('', views.list, name = 'List'),
		path('add/', views.add, name = 'Add complain'),
        path('search/', views.search, name = 'Search'),
        path('<str:id_no>/', views.detail, name = 'Detail View'),
        path('<str:id_no>/accept/', views.accept, name = "Accept Complain" ),
        path('<str:id_no>/add-note/', views.add_note, name = 'Add Note'),
        path('<str:id_no>/approve-redressal/', views.approve_redressal, name = 'Approve Redressal'),
        path('<str:id_no>/deselect/', views.deselect, name = 'Deselect'),
        path('<str:id_no>/edit/', views.edit, name = 'Edit Complain' ),
        path('<str:id_no>/pin/', views.pin_complain, name = 'Pin Complain'),
        path('<str:id_no>/redress/', views.redress, name = 'Complain Redress'),
        path('<str:id_no>/reject/', views.reject, name = 'Reject Complain' ),
        path('<str:id_no>/reject-redressal/', views.reject_redressal, name = 'Reject Redressal'),
        path('<str:id_no>/select/', views.select, name = 'Select'),
        path('<str:id_no>/unpin/', views.unpin_complain, name = "Unpin_Complain")
]
