from django.db import models
import uuid
from django.contrib.auth.models import User
from .validators import file_size
class Post(models.Model):
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    media = models.FileField(upload_to="user-uploads", null=True, blank=True, validators=[file_size])
    body = models.TextField()
    tags= models.ManyToManyField('Tag')
    likes = models.ManyToManyField(User, related_name="likedposts", through="LikedPost")
    created = models.DateTimeField(auto_now_add=True)
    id=models.CharField(max_length=100, unique=True, default=uuid.uuid4, primary_key=True, editable=False)
    
    def __str__(self):
        return str(self.title)
    class Meta:
        ordering = ['-created']

class Tag(models.Model):
    name = models.CharField(max_length=20, null=True, blank=True)
    slug = models.SlugField(max_length=20, unique=True, null=True, blank=True)
    image = models.ImageField(upload_to="category_images", null=True, blank=True)
    order  = models.IntegerField(null=True)

    @property
    def imageURL(self):
        try:
            url=self.image.url
        except:
            url=''
        return url
            
            
    def __str__(self):
        return str(self.name)
    class Meta:
        ordering = ['order']


class LikedPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user.username} : {self.post.title}'

class PostComment(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="comments")
    parent_post= models.ForeignKey(Post, on_delete=models.CASCADE, related_name= "comments")
    body = models.CharField(max_length=150)
    likes = models.ManyToManyField(User, related_name="likedpostcomments", through="LikedPostComment")
    created = models.DateTimeField(auto_now_add=True)
    id = models.CharField(max_length=100, primary_key=True, unique=True, editable=False, default=uuid.uuid4)
     
    def __str__(self):
        try:
            return f'{self.author.username}:{self.body[:30]}'
        except:
            return f'No author : {self.body[:30]}' 
    class Meta:
        ordering = ['-created']

class LikedPostComment(models.Model):
    comment = models.ForeignKey(PostComment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user.username} : {self.comment}'        

class PostCommentReply(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="replies")
    parent_comment = models.ForeignKey(PostComment, on_delete=models.CASCADE, related_name= "replies")
    body = models.CharField(max_length=150)
    likes = models.ManyToManyField(User, related_name="likedpostcommentsreplies", through="LikedPostCommentReply")
    created = models.DateTimeField(auto_now_add=True)
    id = models.CharField(max_length=100, primary_key=True, unique=True, editable=False, default=uuid.uuid4)
     
    def __str__(self):
        try:
            return f'{self.author.username}:{self.body[:30]}'
        except:
            return f'no author:{self.body[:30]}'  
    class Meta:
        ordering = ['-created']

class LikedPostCommentReply(models.Model):
    reply = models.ForeignKey(PostCommentReply, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user.username} : {self.reply}'
    
class Repost(models.Model):
    id = models.CharField(max_length=100, null=False, blank=False, unique=True, default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    original_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date_reposted = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user } reposted { self.original_post.title} on { self.date_reposted }'
    
    class Meta:
        ordering =['-date_reposted']