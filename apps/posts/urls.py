from django.urls import path
from .views import post_list, single_post

urlpatterns = [
    path('', post_list, name='post_list'),
    path('<int:post_id>/', single_post, name='post_detail'),
]