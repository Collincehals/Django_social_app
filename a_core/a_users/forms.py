from django import forms
from django.forms import ModelForm
from .models import Profile


class ProfileEditForm(ModelForm):
    class Meta:
        model = Profile
        
        exclude = ['user','followers']
        labels = {
            'realname': 'First Name',
            'image': 'Profile Photo',
            'profilebackground': 'Background',
        }
        
        widgets = {
            'image': forms.FileInput(),
            'profilebackground': forms.FileInput(),
            'bio': forms.Textarea(attrs={'rows':3}),
        }
    