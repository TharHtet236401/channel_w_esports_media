from django.shortcuts import render
from .models import Post
from .selectors import get_posts

# Create your views here.
def post_list(request):
    posts = get_posts()
    return render(request, 'posts/post_list.html', {'posts': posts})