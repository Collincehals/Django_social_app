from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from posts_app.models import Post
from django.contrib.auth import login, logout, authenticate
from django.db.models import Count
from posts_app.forms import PostCommentReplyForm
# Create your views here.


def ProfileView(request, username=None):
    if username:
        user = get_object_or_404(User, username=username)
        profile = user.profile
        #posts = Post.objects.filter(author=user)
    else:
        try:
            profile = request.user.profile
            #posts = Post.objects.filter(author=request.user)
        except:
            raise Http404()
    posts = profile.user.posts.all()
    if request.htmx:
        if 'top-posts' in request.GET:
            posts = profile.user.posts.annotate(num_likes=Count('likes')).filter(num_likes__gt=0).order_by('-num_likes')
            return render(request, 'snippets/loop_profile_posts.html',{'posts': posts})
        elif 'top-comments' in request.GET:
            comments = profile.user.comments.annotate(num_likes=Count('likes')).filter(num_likes__gt=0).order_by('-num_likes')
            replyform = PostCommentReplyForm()
            return render(request, 'snippets/loop_profile_comments.html',{'comments': comments, 'replyform': replyform})
        else:
            return render(request, 'snippets/loop_profile_posts.html',{'posts': posts})
    
    context = {
        'profile': profile,
        'posts': posts,
    }
    return render(request, 'a_users/profile.html', context)


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