from django.forms import ModelForm
from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError


class SignUpForm(UserCreationForm):
    email = forms.EmailField (required=True)
    first_name = forms.CharField (required=True)
    last_name = forms.CharField (required=True)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2'] 
    
class CreatePostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['media', 'body', 'tags']
        labels = {
            'body': '',
            'media':'Attach file',
            'tags': 'Category'
        }
        widgets = {
        'body': forms.Textarea (attrs={'rows':3, 'placeholder':'Go ahead, tell your story...'}),
        'media': forms.FileInput(),
        'tags':forms.CheckboxSelectMultiple(),
        }

class PostEditForm(ModelForm):
    class Meta:
        model = Post
        fields = ['body','tags']
        labels = {
            'body':'',
            'tags': 'Category' 
        }
        widgets = {
            'body': forms.Textarea (attrs={'rows':5}),
            'tags':forms.CheckboxSelectMultiple(),
        }  
        
          
class PostCommentForm(ModelForm):
    class Meta:
        model = PostComment
        fields = ['body']
        labels = {
            'body': ''
        }
        widgets = {
            'body': forms.TextInput(attrs={'placeholder':'Post Comment...'}),
        }
        
class PostCommentReplyForm(ModelForm):
    class Meta:
        model = PostCommentReply
        fields = ['body']
        labels = {
            'body': ''
        }
        widgets = {
            'body': forms.TextInput(attrs={'placeholder':'Post Reply...' }),
        }  