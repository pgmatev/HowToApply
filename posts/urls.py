from . import views
from django.urls import path

app_name = "posts"

urlpatterns = [
    path('post/create', views.create_post, name='create_post'),
    path('posts/<slug>', views.view_post, name='view_post'),
    path('post/update/<slug>', views.update_post, name='update_post'),
    path('post/delete/<slug>', views.delete_post, name='delete_post')
]
