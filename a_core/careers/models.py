from django.db import models
import uuid

# Create your models here.

class Post(models.Model):
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