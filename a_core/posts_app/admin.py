from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Post)
admin.site.register(Note)
admin.site.register(LikedPost)
admin.site.register(LikedNote)
admin.site.register(PostComment)
admin.site.register(PostCommentReply)
admin.site.register(LikedPostComment)
admin.site.register(LikedPostCommentReply)