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
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model
from posts_app.models import Repost


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
    post_count = len(posts)
    following_users = profile.user.following.all()
    users = User.objects.all().exclude(id=request.user.id).exclude(is_superuser=True).exclude(pk__in=following_users)
    followers = profile.followers.all()
    following = profile.user.following.all()
    
    context = {
        'profile': profile,
        'posts': posts,
        'post_count': post_count,
        'users': users,
        'following': following,
        'followers': followers,
    }
    if request.htmx:
        if 'top-posts' in request.GET:
            posts = profile.user.posts.annotate(num_likes=Count('likes')).filter(num_likes__gt=0).order_by('-num_likes')
            return render(request, 'snippets/loop_profile_posts.html',{'posts': posts,})
        elif 'top-comments' in request.GET:
            comments = profile.user.comments.annotate(num_likes=Count('likes')).filter(num_likes__gt=0).order_by('-num_likes')
            commentreplyform = PostCommentReplyForm()
            return render(request, 'snippets/loop_profile_comments.html',{'comments': comments, 'commentreplyform': commentreplyform})
        elif 'reposts' in request.GET:
             reposts = Repost.objects.filter(user=profile.user)
             return render(request, 'snippets/loop_profile_reposts.html',{'reposts':reposts})
        else:
            return render(request, 'snippets/loop_profile_posts.html',context)
    
    return render(request, 'a_users/profile.html', context)

@login_required
@require_POST
def follow_user(request, username):
    user_to_follow = get_object_or_404(get_user_model(), username=username)
    user_to_follow_profile = user_to_follow.profile
    if user_to_follow == request.user:
        messages.error(request, "You cannot follow yourself.")
    elif request.user in user_to_follow_profile.followers.all():
        messages.info(request, f"You are already following {user_to_follow}.")
    else:
        user_to_follow_profile.followers.add(request.user)
        messages.success(request, f"You are now following {user_to_follow}.")
    return redirect(reverse('userprofile', kwargs={'username': username}))


@login_required
@require_POST
def unfollow_user(request, username):
    if request.method == 'POST':
        user_to_unfollow = get_object_or_404(get_user_model(), username=username)
        if request.user in user_to_unfollow.profile.followers.all():
            user_to_unfollow.profile.followers.remove(request.user)
            messages.success(request, f'You have unfollowed {user_to_unfollow}')
        return redirect('userprofile', username=username)
                             
                             
@login_required
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


@login_required
def followview(request, username):
    target_user = get_object_or_404(get_user_model(), username=username)
    profile = target_user.profile
    followers = target_user.profile.followers.all().exclude(id=request.user.id)
    following = target_user.following.all().exclude(id=request.user.id)
    users = User.objects.exclude(username=request.user.username).exclude(is_superuser=True)
    
    if request.htmx:
        if 'following' in request.GET:
            following = target_user.following.all().exclude(id=request.user.id)
            return render(request, 'snippets/loop_following.html',{'following': following})
        else:    
            followers = target_user.profile.followers.all().exclude(id=request.user.id)
            return render(request, 'snippets/loop_followers.html',{'followers': followers})
    
    context = {
        'users': users,
        'profile': profile,
        'followers': followers,
        'following': following,
    }
    return render(request, 'a_users/follow_page.html',context)

@login_required
def site_users_view(request):
    following_users= request.user.following.all()
    site_users = User.objects.exclude(pk=request.user.pk).exclude(is_superuser=True).exclude(pk__in = following_users)
    return render(request, 'a_users/users.html', {'site_users':site_users})