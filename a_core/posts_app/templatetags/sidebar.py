from django.template import Library
from ..models import Tag, Post, PostComment
from django.db.models import Count

#Instance of the library
register = Library()

@register.inclusion_tag('includes/sidebar.html')
def sidebar_view(tag=None, user=None):
      categories = Tag.objects.all()
      top_posts = Post.objects.annotate(num_likes=Count('likes')).filter(num_likes__gt=2).order_by('-num_likes')
      top_comments = PostComment.objects.annotate(num_likes=Count('likes')).filter(num_likes__gt=1).order_by('-num_likes')
      context = {
          'categories': categories,
          'tag': tag,
          'top_posts': top_posts,
          'user': user,
          'top_comments':top_comments,
      }
      return context