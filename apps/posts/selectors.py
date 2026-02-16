from .models import Post


def get_posts(region_name=None):
    try:
        qs = Post.objects.prefetch_related("region").order_by("-created_at")
        if region_name:
            qs = qs.filter(region__name=region_name)
        return qs
    except Exception as e:
        print(e)
        return []