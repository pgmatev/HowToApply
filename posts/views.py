from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required

from .models import Post
from .forms import PostForm
import datetime


@login_required
def create_post(request):
    user = request.user
    post_form = PostForm()

    if user:
        if hasattr(user, 'university'):
            if request.method == 'POST':
                post_form = PostForm(request.POST)

                if post_form.is_valid():
                    post = post_form.save(commit=False)
                    post.author = user.university
                    post.created_at = datetime.datetime.now()
                    post.save()
                    return redirect('posts:view_post', slug=post.slug)

            context = {'form': post_form}
            return render(request, 'posts/create_post.html', context)


def view_post(request, *args, **kwargs):
    post_slug = kwargs.get("slug")

    try:
        post = Post.objects.get(slug=post_slug)
    except Post.DoesNotExist():
        return HttpResponse("Post doesn't exist")

    if post:
        context = {'post': post}
        return render(request, 'posts/view_post.html', context)


@login_required
def update_post(request, *args, **kwargs):
    post_slug = kwargs.get("slug")
    user = request.user

    try:
        post = Post.objects.get(slug=post_slug)
    except Post.DoesNotExist():
        return HttpResponse("Post doesn't exist")

    if post and user == post.author.user:
        post_form = PostForm(instance=post)

        if request.method == 'POST':
            post_form = PostForm(request.POST, instance=post)

            if post_form.is_valid():
                post = post_form.save(commit=False)
                post.updated_at = datetime.datetime.now()
                post.save()
                return redirect('posts:view_post', slug=post.slug)
        context = {'form': post_form, 'post': post}
        return render(request, 'posts/update_post.html', context)


@login_required
def delete_post(request, slug):
    Post.objects.filter(slug=slug).delete()
    return redirect('home')
