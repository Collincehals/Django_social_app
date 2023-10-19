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
    likes = models.ManyToManyField(User, related_name="likedposts", through="LikedPost")
    created = models.DateTimeField(auto_now_add=True)
    id=models.CharField(max_length=100, unique=True, default=uuid.uuid4, primary_key=True, editable=False)
    
    def __str__(self):
        return str(self.title)
    
    class Meta:
        ordering = ['-created']


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="comments")
    parent_post= models.ForeignKey(Post, on_delete=models.CASCADE, related_name= "comments")
    body = models.CharField(max_length=150)
    created = models.DateTimeField(auto_now_add=True)
    id = models.CharField(primary_key=True, max_length=50, unique=True, editable=False, default=uuid.uuid4)
     
    def __str__(self):
        try:
            return f'{self.auther.username}:{self.body[:30]}'
        except:
            return f'no author:{self.body[:30]}'




class LikedPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user.username} : {self.post.title}'
     
        
class Note(models.Model):
    author = models.ForeignKey(User,null=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=False)
    description = models.TextField()
    likes = models.ManyToManyField(User, related_name='likednotes', through='LikedNote')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title + "\n" + self.description
    class Meta:
        ordering = ['-created_at']  
    
        
class LikedNote(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user.username} : {self.note.title}'
    