from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .forms import PostForm
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


def post_admin_dashboard(request):
    try:
        posts = (
            Post.objects.all()
            .prefetch_related("region")
            .order_by("-created_at")
        )
        form = PostForm()
        context = {
            "posts": posts,
            "form": form,
        }
        return render(request, "posts/admin/dashboard.html", context)
    except Exception as e:
        return render(
            request,
            "posts/admin/dashboard.html",
            {"posts": [], "form": None, "error": str(e)},
        )


def post_admin_list(request):
    try:
        posts = (
            Post.objects.all()
            .prefetch_related("region")
            .order_by("-created_at")
        )
        return render(
            request,
            "posts/admin/partials/post_table.html",
            {"posts": posts},
        )
    except Exception as e:
        return render(
            request,
            "posts/admin/partials/post_table.html",
            {"posts": [], "error": str(e)},
        )


def post_admin_create(request):
    try:
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                form.save()
                posts = (
                    Post.objects.all()
                    .prefetch_related("region")
                    .order_by("-created_at")
                )
                if request.headers.get("HX-Request"):
                    return render(
                        request,
                        "posts/admin/partials/post_table.html",
                        {"posts": posts},
                    )
                return redirect("post_admin_dashboard")
        else:
            form = PostForm()

        form_action = reverse("post_admin_create")
        template = (
            "posts/admin/partials/post_form.html"
            if request.headers.get("HX-Request")
            else "posts/admin/dashboard.html"
        )
        context = {"form": form, "form_action": form_action}
        return render(request, template, context)
    except Exception as e:
        form = PostForm()
        template = (
            "posts/admin/partials/post_form.html"
            if request.headers.get("HX-Request")
            else "posts/admin/dashboard.html"
        )
        return render(
            request,
            template,
            {"form": form, "form_action": reverse("post_admin_create"), "error": str(e)},
        )


def post_admin_update(request, post_id):
    try:
        post = get_object_or_404(Post, id=post_id)
        if request.method == "POST":
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                form.save()
                posts = (
                    Post.objects.all()
                    .prefetch_related("region")
                    .order_by("-created_at")
                )
                if request.headers.get("HX-Request"):
                    return render(
                        request,
                        "posts/admin/partials/post_table.html",
                        {"posts": posts},
                    )
                return redirect("post_admin_dashboard")
        else:
            form = PostForm(instance=post)

        form_action = reverse("post_admin_update", args=[post_id])
        template = "posts/admin/partials/post_form.html"
        return render(
            request,
            template,
            {"form": form, "form_action": form_action, "post": post},
        )
    except Exception as e:
        form = PostForm()
        return render(
            request,
            "posts/admin/partials/post_form.html",
            {
                "form": form,
                "form_action": reverse("post_admin_create"),
                "error": str(e),
            },
        )


def post_admin_delete(request, post_id):
    try:
        if request.method == "POST":
            post = get_object_or_404(Post, id=post_id)
            post.delete()
        posts = (
            Post.objects.all()
            .prefetch_related("region")
            .order_by("-created_at")
        )
        return render(
            request,
            "posts/admin/partials/post_table.html",
            {"posts": posts},
        )
    except Exception as e:
        return render(
            request,
            "posts/admin/partials/post_table.html",
            {"posts": [], "error": str(e)},
        )


def post_admin_detail(request, post_id):
    try:
        post = get_object_or_404(Post.objects.prefetch_related("region"), id=post_id)
        return render(
            request,
            "posts/admin/partials/post_detail.html",
            {"post": post},
        )
    except Exception as e:
        return render(
            request,
            "posts/admin/partials/post_detail.html",
            {"post": None, "error": str(e)},
        )