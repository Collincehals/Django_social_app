from django.urls import path
from .views import *

urlpatterns = [
    path('',Inbox, name='inbox'),
    path('c/<conversation_id>/',Inbox, name='inbox'),
    path('search_users/',SearchUsers, name='inbox_search_users'),
    path('create_message/<recipient_id>/',create_message, name='create_message'),
    path('inbox-newreply/<conversation_id>/',new_reply, name='inbox-newreply'),
    path('notify/<conversation_id>/',notify_newmessage, name='notify-newmessage'),
    path('notify-inbox/', notify_inbox, name='notify-inbox'),    
]