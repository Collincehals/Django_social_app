from django.shortcuts import render, redirect
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def ProfileView(request):
    profile = request.user.profile
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
    profile = request.user.profile
    if request.method == 'POST':
        profile.delete()
        messages.success(request, "Profile deleted successfully")
        return redirect('home')
    return render(request, 'a_users/delete_profile.html')