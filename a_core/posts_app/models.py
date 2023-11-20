from django.db import models
import uuid
from django.contrib.auth.models import User

class Post(models.Model):
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    image = models.URLField(max_length=200, null=True)
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
    name = models.CharField(max_length=20)
    slug = models.SlugField(max_length=20, unique=True)
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
    id = models.CharField(primary_key=True, max_length=50, unique=True, editable=False, default=uuid.uuid4)
     
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
    id = models.CharField(primary_key=True, max_length=50, unique=True, editable=False, default=uuid.uuid4)
     
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



#NOTES MODELS        
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
    