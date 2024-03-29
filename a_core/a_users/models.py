from django.db import models
from django.contrib.auth.models import User
from django_resized import ResizedImageField
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = ResizedImageField(size=[600, 600],quality=85, upload_to='profilepics/', blank=True, null=True)
    profilebackground = ResizedImageField(size=[1200, 1200], quality=70, upload_to='profilepics/', blank=True, null=True)
    realname = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=50, unique=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    followers = models.ManyToManyField(User, blank=True, related_name="following")
    bio = models.TextField(max_length=500, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.user)
    
    @property
    def imageURL(self):
        try:
            url=self.image.url
        except:
            url=''
        return url
    
    @property
    def profilebackgroundURL(self):
        try:
            url=self.profilebackground.url
        except:
            url=''
        return url
        
            
            