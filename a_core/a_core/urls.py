"""
URL configuration for a_core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin 
from django.urls import path, include
from posts_app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),
    path("", home_view, name= "home"),
    path('home/', home_view, name='home'),
    path('post/create/',create_post_view, name="post-create"),
    path('sign-up/',signup_view, name="sign-up"),
    path('note/create/',CreateNoteView, name="note-create"),
    path('notes/',NotesView, name="notes"),
    path('delete/note/<pk>/',NoteDeleteView, name="delete-note"),
    path('delete/post/<pk>/',PostDeleteView, name="delete-post"),
    path('post/edit/<pk>/',PostEditView, name="edit-post"),
    path('note/edit/<pk>/',NoteEditView, name="edit-note"),
    path('post/<pk>/',PostView, name="view-post"),
]