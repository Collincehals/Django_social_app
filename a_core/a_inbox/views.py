from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
@login_required
def Inbox(request):
    conversation = Conversation.objects.first()
    context = {
        'conversation': conversation,
    }
    return render(request, 'a_inbox/inbox.html', context)