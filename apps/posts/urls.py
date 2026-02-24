from django.urls import path

from .views import (
    post_list,
    single_post,
    post_admin_dashboard,
    post_admin_list,
    post_admin_create,
    post_admin_update,
    post_admin_delete,
    post_admin_detail,
)


urlpatterns = [
    path("", post_list, name="post_list"),
    path("<int:post_id>/", single_post, name="post_detail"),
    path("admin/posts/", post_admin_dashboard, name="post_admin_dashboard"),
    path("admin/posts/list/", post_admin_list, name="post_admin_list"),
    path("admin/posts/create/", post_admin_create, name="post_admin_create"),
    path("admin/posts/<int:post_id>/edit/", post_admin_update, name="post_admin_update"),
    path("admin/posts/<int:post_id>/delete/", post_admin_delete, name="post_admin_delete"),
    path("admin/posts/<int:post_id>/detail/", post_admin_detail, name="post_admin_detail"),
]