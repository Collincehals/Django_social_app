from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import PasswordResetForm, PasswordChangeForm
from django.contrib import messages


# Create your views here.
def home_view(request):
    posts = Post.objects.all()
    return render(request, 'a_posts/home.html', {'posts': posts})

#POSTS VIEWS
@login_required(login_url="account_login")      
def create_post_view(request):
    form = CreatePostForm ()
    if request.method == 'POST':
        form = CreatePostForm(request.POST)
        if form.is_valid():
            post = form.save(commit= False)
            post.author = request.user
            post.save()
            messages.success(request,'Post created successfully!')
            return redirect('home')
    return render(request, 'a_posts/create_post.html', {'form': form})

def PostView(request, pk):
    post = Post.objects.get(id=pk)
    commentform = PostCommentForm()
    commentreplyform = PostCommentReplyForm
    context = {
        'post': post, 
        'commentform': commentform,
        'commentreplyform': commentreplyform,
        }
    return render(request, 'a_posts/post_page.html', context)


def PostEditView(request, pk):
    post = Post.objects.get(id=pk)
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

def like_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    user_exists = post.likes.filter(username=request.user.username).exists()
    
    if post.author != request.user:
        if user_exists:
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
    return render(request, 'snippets/posts_likes.html', {'post': post})


@login_required(login_url='account_login')
def post_comment_sent_view(request, pk):
    post= get_object_or_404(Post,id=pk)
    if request.method == 'POST':
        form = PostCommentForm(request.POST)
        if  form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.parent_post = post
            comment.save()
    return redirect('view-post', post.id)

def post_comment_like_view(request, pk):
    comment = get_object_or_404(PostComment, id=pk)
    user_exists = comment.likes.filter(username=request.user.username).exists()
    
    if comment.author != request.user:
        if user_exists:
            comment.likes.remove(request.user)
        else:
            comment.likes.add(request.user)
    return render(request, 'snippets/posts_comment_likes.html', {'comment': comment})


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
    if request.method == 'POST':
        form = PostCommentReplyForm(request.POST)
        if  form.is_valid():
            reply = form.save(commit=False)
            reply.author = request.user
            reply.parent_comment = comment
            reply.save()
    return redirect('view-post', comment.parent_post.id) 

def post_comment_reply_like_view(request, pk):
    reply = get_object_or_404(PostCommentReply, id=pk)
    user_exists = reply.likes.filter(username=request.user.username).exists()
    
    if reply.author != request.user:
        if user_exists:
            reply.likes.remove(request.user)
        else:
            reply.likes.add(request.user)
    return render(request, 'snippets/post_comment_reply_likes.html', {'reply': reply})


@login_required(login_url='account_login')
def PostCommentReplyDeleteView(request, pk):
    reply = get_object_or_404(PostCommentReply, id=pk, author=request.user)
    if request.method == 'POST':
        reply.delete()
        messages.success(request, 'Reply deleted!')
        return redirect('view-post',reply.parent_comment.parent_post.id)
    return render(request, 'a_posts/post_comment_reply_delete.html', {'reply': reply})


#NOTES VIEWS
@login_required(login_url='account_login')
def CreateNoteView(request):
    form = CreateNote()
    if request.method == 'POST':
        form = CreateNote(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.author  = request.user
            note.save()
            messages.success(request,'Note created successfully!')
            return redirect('notes')
    else:
        form = CreateNote()
    return render(request, 'a_posts/create_notes.html', {'form': form})

def NotesView(request):
    notes = Note.objects.all()
    return render(request, 'a_posts/notes.html', {'notes': notes})

def NoteEditView(request, pk):
    note = Note.objects.get(id=pk)
    form = NoteEditForm(instance=note)
    if request.method == 'POST':
        form = NoteEditForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request,'Note updated successfully!')
            return redirect('notes')
    context = {
        'note': note,
        'form': form
    }
    return render(request, 'a_posts/note_edit.html', context)

def NoteDeleteView(request,pk):
    note  = Note.objects.get(id=pk)
    if request.method == 'POST':
        note.delete()
        messages.success(request,'Note deleted successfully')
        return redirect('notes')
    return render(request, 'a_posts/note_delete.html', {'note': note})

def like_note (request, pk):
    note = get_object_or_404(Note, id=pk)
    user_exists = note.likes.filter(username=request.user.username).exists()
    if note.author != request.user:
        if user_exists:
            note.likes.remove(request.user)
        else:
            note.likes.add(request.user)
    return render(request, 'snippets/notes_likes.html',{'note':note})


        












from django.core.mail import send_mail
def send_email_view(request):
    user_email = request.POST.get('email') or request.session.get('email')
    send_mail(
        'Hello from Colltech Team',
        'This is a test email from Colltech.',
        'colltechcareers@gmail.com',
        [user_email],
        fail_silently=False,
    )
    return HttpResponse('Email sent successfully.')