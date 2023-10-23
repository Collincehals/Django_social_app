from django import forms
from django.forms import ModelForm
from .models import Profile


class ProfileEditForm(ModelForm):
    class Meta:
        model = Profile
        
        exclude = ['user']
        labels = {
            'realname': 'First Name',
            'image': 'Profile Photo',
        }
        
        widgets = {
            'image': forms.FileInput(),
            'bio': forms.Textarea(attrs={'rows':3})
        }
    