from django.urls import path

from . import views

urlpatterns = [
	path('', views.list, name = 'Thread List'),
	path('add/', views.add_thread, name = 'Add Thread'),
	path('load-categories/', views.load_categories, name = 'Load Categories' ),
	path('load-subcategories/', views.load_subcategories, name = 'Load SubCategories'),
	path('search-filter/', views.search_filter, name = 'Search&Filter Thread'),
	path('<str:id_no>/', views.detail, name = 'Thread Detail'),
	path('<str:id_no>/add-note/', views.add_note, name = 'Thread Add Note'),
	path('<str:id_no>/add-redressal/',views.add_redressal, name = 'Thread Redressal'),
	path('<str:id_no>/attach-complain/<str:complain_id>/',
		views.attach_complain, name = 'Attach Complain'
	),
	path('<str:id_no>/approve/', views.approve_redressal, name = 'Approve Thread'),
	path('<str:id_no>/deselect/', views.deselect_to_solve, name = 'Deselect Thread' ),
	path('<str:id_no>/reject-approval/', views.reject_redressal, name = 'Reject Thread Redressal'),
	path('<str:id_no>/select-to-solve/', views.select_to_solve, name= 'Select Thread'),
]
