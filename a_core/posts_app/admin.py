from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Post)
admin.site.register(LikedPost)
admin.site.register(PostComment)
admin.site.register(PostCommentReply)
admin.site.register(LikedPostComment)
admin.site.register(LikedPostCommentReply)
admin.site.register(Tag)
admin.site.register(Repost)