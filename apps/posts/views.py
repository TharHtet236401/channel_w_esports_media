from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404

from .models import Post, Region
from .selectors import get_posts

def post_list(request):
    try:
        region_name = request.GET.get("region", "").strip() or None
        post_list_qs = get_posts(region_name=region_name)
        paginator = Paginator(post_list_qs, 9)
        page_number = request.GET.get("page", 1)
        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        regions = Region.objects.all().order_by("name")
        context = {
            "posts": page_obj.object_list,
            "page_obj": page_obj,
            "regions": regions,
            "current_region": region_name,
        }
        if request.headers.get("HX-Request"):
            return render(
                request,
                "posts/partials/post_list_content.html",
                context,
            )
        return render(request, "posts/post_list.html", context)
    except Exception as e:
        context = {
            "posts": [],
            "page_obj": None,
            "regions": [],
            "current_region": None,
            "error": str(e),
        }
        if request.headers.get("HX-Request"):
            return render(request, "posts/partials/post_list_content.html", context)
        return render(request, "posts/post_list.html", context)

def single_post(request, post_id):
    try:
        post = get_object_or_404(Post.objects.prefetch_related("region"), id=post_id)
        return render(request, "posts/single_post.html", {"post": post})
    except Exception as e:
        return render(request, "posts/single_post.html", {"post": None, "error": str(e)})