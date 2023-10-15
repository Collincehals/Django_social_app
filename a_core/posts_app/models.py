from django.db import models
import uuid
from django.contrib.auth.models import User
# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200, null=True)
    url = models.URLField(max_length=200, null=True)
    image = models.URLField(max_length=200)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    id=models.CharField(max_length=100, unique=True, default=uuid.uuid4, primary_key=True, editable=False)
    
    def __str__(self):
        return str(self.title)
    
    class Meta:
        ordering = ['-created']
        
        
class Note(models.Model):
    author = models.ForeignKey(User,null=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=False)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title + "\n" + self.description
    class Meta:
        ordering = ['-created_at']      