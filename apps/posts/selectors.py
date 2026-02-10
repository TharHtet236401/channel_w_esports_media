from .models import Post

def get_posts():
    try:
        posts = Post.objects.all()
        return posts
    except Exception as e:
        print(e)
        return []