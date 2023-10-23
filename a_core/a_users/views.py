from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.contrib.auth import login, logout, authenticate
# Create your views here.
def ProfileView(request, username=None):
    if username:
        profile = get_object_or_404(User, username=username).profile
    else:
        try:
            profile = request.user.profile
        except:
            raise Http404()
    return render(request, 'a_users/profile.html', {"profile": profile})


def EditProfileView(request):
    form = ProfileEditForm(instance=request.user.profile)
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile has been updated')
            return redirect('view-profile')
        else:
            messages.error(request, 'Error updating profile')
            return redirect('edit-profile')
    return render(request, 'a_users/edit_profile.html',{"form": form})


def DeleteProfileView(request):
   user = request.user
   if request.method == 'POST':
       logout(request)
       user.delete()
       messages.success(request, "Profile deleted successfully")
       return redirect('home')
   return render(request, 'a_users/delete_profile.html')