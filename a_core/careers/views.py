from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import PasswordResetForm, PasswordChangeForm



# Create your views here.
def home_view(request):
    posts = Post.objects.all()
    notes = Notes.objects.all()
    return render(request, 'a_posts/home.html', {'posts': posts, 'notes': notes})

@login_required(login_url="login")      
def create_post_view(request):
    form = CreatePostForm ()
    if request.method == 'POST':
        form = CreatePostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'a_posts/create_post.html', {'form': form})

def signup_view(request):
    form = SignUpForm ()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    return render(request, 'registration/sign-up.html', {'form': form})

def Password_change_view(request):
    form = PasswordChangeForm ()
    return render(request, 'registration/password_change_form.html', {'form': form})


def Password_reset_view(request):
    form = PasswordResetForm()
    return render(request, 'registration/password_reset_form.html', {'form': form})

def PasswordChangeDoneView(request):
    return render(request, 'registration/password_change_done.html')

@login_required(login_url='login')
def CreateNotesView(request):
    form = CreateNotes
    if request.method == 'POST':
        form = CreateNotes(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.author  = request.user
            note.save()
            return redirect('home')
    else:
        form = CreateNotes()
    return render(request, 'a_posts/create_notes.html', {'form': form})