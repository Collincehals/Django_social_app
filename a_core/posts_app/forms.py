from django.forms import ModelForm
from django import forms
from .models import *

#for user registration
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
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        return email


class CreatePostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'image', 'body']
        labels = {
            'body': 'Caption',
            'image':'Image URL',
        }
        widgets = {
        'body': forms.Textarea (attrs={'rows':3, 'placeholder':'Enter Caption here...', 'class': 'font1 text 4xl' }),
        'image': forms.TextInput (attrs={'placeholder':'Enter URL here...'})
        }
        
class PostCommentForm(ModelForm):
    class Meta:
        model = PostComment
        fields = ['body']
        labels = {
            'body': ''
        }
        widgets = {
            'body': forms.TextInput(attrs={'placeholder':'Enter Comment here...' }),
        }
        
class PostCommentReplyForm(ModelForm):
    class Meta:
        model = PostCommentReply
        fields = ['body']
        labels = {
            'body': ''
        }
        widgets = {
            'body': forms.TextInput(attrs={'placeholder':'Enter Reply here...' }),
        }  
        
class PostEditForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body',]
        labels = {
            'body':'',
            'title': '',  
        }
        widgets = {
            'body': forms.Textarea (attrs={'rows':5, 'placeholder':'Enter Caption here...', 'class': 'font1 text 4xl' }),
        }
  
class CreateNote (ModelForm):
    class Meta:
        model = Note
        fields = ["title", "description",]
        
        widgets = {
            'title': forms.TextInput(attrs={'placeholder':'Enter title...'}),
            'description': forms.Textarea(attrs={'placeholder':'Enter your note here...', 'rows':6})
        }
        
class NoteEditForm(ModelForm):
    class Meta:
        model = Note
        fields = ['title','description', ]
        
        widgets = {
            'description': forms.Textarea(attrs={'rows':6})
        }