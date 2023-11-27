from django.contrib import admin
from .models import *

class InboxMessageAdmin(admin.ModelAdmin):
    readonly_fields = ('sender', 'body', 'conversation')
# Register your models here.
admin.site.register(Conversation)
admin.site.register(InboxMessage, InboxMessageAdmin)