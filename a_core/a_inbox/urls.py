from django.urls import path
from .views import *

urlpatterns = [
    path('',Inbox, name='inbox'),
    path('c/<conversation_id>/',Inbox, name='inbox'),
]