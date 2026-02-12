from .models import Post

def get_posts():
    try:
        posts = Post.objects.prefetch_related('region').order_by('-created_at')
        return posts
    except Exception as e:
        print(e)
        return []