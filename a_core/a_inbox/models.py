from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.timesince import timesince
import uuid
from django.conf import settings
from cryptography.fernet import Fernet
# Create your models here.
class InboxMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    conversation = models.ForeignKey('Conversation', on_delete=models.CASCADE,related_name='messages')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        time_since = timesince(self.created_at, timezone.now())
        return f'[{self.sender.username}: {time_since} ago]'
    
    @property
    def body_decrypted(self):
        f = Fernet(settings.ENCRYPT_KEY)
        message_decrypted = f.decrypt(self.body)
        message_decoded = message_decrypted.decode('utf-8')
        return message_decoded
    
class Conversation(models.Model):
    id =models.CharField(max_length=100,default=uuid.uuid4,unique=True, editable=False,primary_key=True)
    participants = models.ManyToManyField(User, related_name="conversations")
    lastmessage_created = models.DateTimeField(default=timezone.now)
    is_seen = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-lastmessage_created']
    
    def __str__(self):
        user_names =", ".join(user.username for user in self.participants.all())
        return f'[{user_names}]'