from django.urls import path, include
from django.contrib import admin
from chat.views import *

urlpatterns=[
    path('', chatbox, name="chatbox"),
    path('search/', chatsearch, name="chatsearch"),
    # path('<str:sid>/', chatpage, name="chatpage"),
    path('chatpage/', chatpage, name="chatpage"),
    path('chatpage1/', chatpage1, name="chatpage1"),
    path('allstudent/', allstudent, name="allstudent"),
    path('studchatbox/', studchatbox, name='studchatbox'),
    path('studchatpage/', studchatpage, name='studchatpage')
]
