from django.urls import path, include
from django.contrib import admin
from chat.views import *

urlpatterns=[
    path('', chatbox, name="chatbox"),
    path('search/', chatsearch, name="chatsearch"),
    path('<str:id>/', chatpage, name="chatpage"),
    path('allstudent/', allstudent, name="allstudent"),
    path('studchatbox/', studchatbox, name='studchatbox'),
    path('<str:id>/student/', studchatpage, name='studchatpage')
]
