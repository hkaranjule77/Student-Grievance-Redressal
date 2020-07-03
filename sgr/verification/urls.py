from django.urls import path

from . import views

urlpatterns = [
        path('add-table/', views.add_table, name = 'Add Table Details'),
         path('dbdetails/',views.db_details,name='DBDetails')
    ]