from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate

# Create your views here.
def home_view(request):
    posts = Post.objects.all()
    return render(request, 'a_posts/home.html', {'posts': posts})

def signup_view(request):
    form = SignUpForm ()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
    return render(request, 'registration/sign-up.html', {'form': form})


@login_required(login_url="login")      
def create_post_view(request):
    form = CreatePostForm ()
    if request.method == 'POST':
        form = CreatePostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'a_posts/create_post.html', {'form': form})

def Password_change_view(request):
    form = CustomPasswordChangeForm ()
    return render(request, 'registration/password_change_form.html', {'form': form})
