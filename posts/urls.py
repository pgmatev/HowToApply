from . import views
from django.urls import path

app_name = "posts"

urlpatterns = [
    path('create', views.create_post, name='create_post'),
    path('<slug>', views.view_post, name='view_post'),
    path('<slug>/update', views.update_post, name='update_post'),
    path('<slug>/delete', views.delete_post, name='delete_post')
]
