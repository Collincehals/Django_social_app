from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Count


# Create your views here.
def home_view(request, tag=None):
    if tag:
        posts = Post.objects.filter(tags__slug=tag)
        tag = get_object_or_404(Tag, slug=tag)
    else:
        posts = Post.objects.all()
    paginator = Paginator(posts, 3)
    page = int(request.GET.get('page', 1))
    try:
        posts = paginator.page(page)
    except:
        return HttpResponse('<div>No more posts</div>')
    context={
        'posts': posts,
        'page': page,
        'tag':tag
        }
     
    if request.htmx:
        return render(request, 'snippets/loops_home_posts.html', context)  
    return render(request, 'a_posts/home.html', context)


#POSTS VIEWS
@login_required(login_url="account_login")      
def create_post_view(request):
    form = CreatePostForm ()
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit= False)
            post.author = request.user
            post.save()
            form.save_m2m()
            messages.success(request,'Post created successfully!')
            return redirect('view-profile')
    return render(request, 'a_posts/create_post.html', {'form': form})

def PostView(request, pk):
    post = get_object_or_404(Post, id=pk)
  
    commentform = PostCommentForm()
    commentreplyform = PostCommentReplyForm
    
    if request.htmx:
        if 'top' in request.GET:
            comments = post.comments.annotate(num_likes=Count('likes')).filter(num_likes__gt=0).order_by('-num_likes')
        else:    
            comments = post.comments.all()
        return render(request, 'snippets/loop_postpage_comments.html', {'comments': comments, 'commentreplyform': commentreplyform})
    
    context = {
        'post': post, 
        'commentform': commentform,
        'commentreplyform': commentreplyform,
        }
    return render(request, 'a_posts/post_page.html', context)


def PostEditView(request, pk):
    post = get_object_or_404(Post, id=pk)
    form = PostEditForm(instance=post)
    if request.method == 'POST':
        form = PostEditForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('home')
    context = {
        'post': post,
        'form': form
        }
    return render(request, 'a_posts/post_edit.html', context)


def PostDeleteView(request, pk):
    post = get_object_or_404(Post, id=pk, author=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('home')
    return render(request, 'a_posts/post_delete.html', {'post': post})

def like_toggle(model):
    def inner_func(func):
        def wrapper(request, *args, **kwargs):
            post = get_object_or_404(model, id=kwargs.get('pk'))
            user_exists = post.likes.filter(username=request.user.username).exists()
            
            if post.author!= request.user:
                if user_exists:
                    post.likes.remove(request.user)
                else:
                    post.likes.add(request.user)
            return func(request,post)
        return wrapper
    return inner_func

#Posts, post comments and post comment replies likes:
  
@like_toggle(Post)
def like_post(request, post):
    return render(request, 'snippets/posts_likes.html', {'post': post})
  
@like_toggle(PostComment)
def post_comment_like_view(request, comment):
    return render(request, 'snippets/posts_comment_likes.html', {'comment': comment})


def post_comment_reply_like_view(request, pk):
    reply = get_object_or_404(PostCommentReply, id=pk)
    user_exists = reply.likes.filter(username=request.user.username).exists()
    
    if reply.author != request.user:
        if user_exists:
            reply.likes.remove(request.user)
        else:
            reply.likes.add(request.user)
    return render(request, 'snippets/post_comment_reply_likes.html', {'reply': reply})
#End likes list

#post-comments here
@login_required(login_url='account_login')
def post_comment_sent_view(request, pk):
    post= get_object_or_404(Post,id=pk)
    commentreplyform = PostCommentReplyForm()
    if request.method == 'POST':
        form = PostCommentForm(request.POST)
        if  form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.parent_post = post
            comment.save()
            messages.success(request,"Comment added successfully")
    context ={
        'comment':comment,
        'post': post,
        'commentreplyform': commentreplyform
    }
    return render(request, 'snippets/add_postcomment.html', context)
    
 
 
def PostCommentDeleteView(request, pk):
    comment = get_object_or_404(PostComment, id=pk, author=request.user)
    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Comment deleted successfully!')
        return redirect('view-post',comment.parent_post.id)
    return render(request, 'a_posts/comment_delete.html', {'comment': comment})

@login_required(login_url='account_login')
def post_comment_reply_sent_view(request, pk):
    comment= get_object_or_404(PostComment,id=pk)
    commentreplyform = PostCommentReplyForm()
    if request.method == 'POST':
        form = PostCommentReplyForm(request.POST)
        if  form.is_valid(): 
            reply = form.save(commit=False)
            reply.author = request.user
            reply.parent_comment = comment
            reply.save()
    context ={
        'comment':comment,
        'reply':reply,
        'commentreplyform': commentreplyform,
    }
    return render(request, 'snippets/add_postcommentreply.html', context)



@login_required(login_url='account_login')
def PostCommentReplyDeleteView(request, pk):
    reply = get_object_or_404(PostCommentReply, id=pk, author=request.user)
    if request.method == 'POST':
        reply.delete()
        messages.success(request, 'Reply deleted!')
        return redirect('view-post',reply.parent_comment.parent_post.id)
    return render(request, 'a_posts/post_comment_reply_delete.html', {'reply': reply})

"""
def like_note (request, pk):
    note = get_object_or_404(Note, id=pk)
    user_exists = note.likes.filter(username=request.user.username).exists()
    if note.author != request.user:
        if user_exists:
            note.likes.remove(request.user)
        else:
            note.likes.add(request.user)
    return render(request, 'snippets/notes_likes.html',{'note':note})
"""