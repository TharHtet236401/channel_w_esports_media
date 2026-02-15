from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404

from .selectors import get_posts
from .models import Post

def post_list(request):
    try:
        post_list_qs = get_posts()
        paginator = Paginator(post_list_qs, 9)
        page_number = request.GET.get("page", 1)
        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        return render(
            request,
            "posts/post_list.html",
            {"posts": page_obj.object_list, "page_obj": page_obj},
        )
    except Exception as e:
        return render(
            request,
            "posts/post_list.html",
            {"posts": [], "page_obj": None, "error": str(e)},
        )

def single_post(request, post_id):
    try:
        post = get_object_or_404(Post.objects.prefetch_related("region"), id=post_id)
        return render(request, "posts/single_post.html", {"post": post})
    except Exception as e:
        return render(request, "posts/single_post.html", {"post": None, "error": str(e)})