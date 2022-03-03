from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q

from .forms import UniversityForm, StudentForm, AuthenticateUserForm, AuthenticateUniversityForm, PostForm
from .models import Student, University, User, Post

from itertools import chain
import datetime


def login_excluded(redirect_to):
    """ This decorator kicks authenticated users out of a view """

    def _method_wrapper(view_method):
        def _arguments_wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(redirect_to)
            return view_method(request, *args, **kwargs)

        return _arguments_wrapper

    return _method_wrapper


# Create your views here.


def home(request):
    user = request.user

    if user:

        if hasattr(user, 'student'):
            context = {'user': user, 'student': user.student}
            return render(request, 'hta_platform/student_home.html', context)

        elif hasattr(user, 'university'):
            posts = Post.objects.filter(author_id=user.university.id)
            context = {'user': user, 'student': user.university, 'posts': posts}
            return render(request, 'hta_platform/university_home.html', context)

        else:
            context = {'user': user}
            # need to pass message
            return render(request, 'hta_platform/home.html', context)


# @login_required(login_url='/')
def profile(request, *args, **kwargs):
    user_id = kwargs.get("user_id")

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist():
        return HttpResponse("User doesn't exist")

    if user:

        if hasattr(user, 'student'):
            context = {'user': user, 'student': user.student}
            return render(request, 'hta_platform/student_profile.html', context)

        elif hasattr(user, 'university'):
            posts = Post.objects.filter(author=user.university)
            context = {'university': user.university, 'posts': posts}
            return render(request, 'hta_platform/university_profile.html', context)

        else:
            context = {'user': user}
            # need to pass message
            return render(request, 'hta_platform/student_home.html', context)


@login_excluded('home')
def student_register(request):
    form = AuthenticateUserForm()
    student_form = StudentForm()

    if request.method == 'POST':
        form = AuthenticateUserForm(request.POST)
        student_form = StudentForm(request.POST)

        if form.is_valid() and student_form.is_valid():
            user = form.save()
            student = student_form.save(commit=False)
            student.user = user
            student.save()
            return redirect('login')

    context = {'form': form, 'student_form': student_form}
    return render(request, 'hta_platform/student_register.html', context)


@login_excluded('home')
def university_register(request):
    form = AuthenticateUniversityForm()
    university_form = UniversityForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        university_form = UniversityForm(request.POST)

        if form.is_valid() and university_form.is_valid():
            user = form.save(commit=False)
            university = university_form.save(commit=False)
            user.is_active = False
            user.save()
            university.user = user
            university.save()
            # messages.success(request, 'Successfully added ' + university_form.cleaned_data.get('username'))
            return redirect('login')

    context = {'form': form, 'university_form': university_form}
    return render(request, 'hta_platform/university_register.html', context)


@login_excluded('home')
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Wrong credentials')

    return render(request, 'hta_platform/login.html')


@login_required
def logout_user(request):
    logout(request)
    return redirect('login')


def search(request, *arg, **kwargs):
    context = {}

    if request.method == 'GET':
        search_query = request.GET.get("q")
        if len(search_query) > 0:
            print(search_query)
            search_students = Student.objects.filter(Q(user__username__icontains=search_query) |
                                                     Q(user__email__icontains=search_query) |
                                                     Q(user__first_name__icontains=search_query) |
                                                     Q(user__last_name__icontains=search_query))
            search_universities = University.objects.filter(Q(user__username__icontains=search_query) |
                                                            Q(name__icontains=search_query))
            print(search_students)
            search_results = list(chain(search_students, search_universities))
            context['search_results'] = search_results
            context['search_query'] = search_query

    return render(request, 'hta_platform/search_results.html', context)


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
                    return redirect('view_post', slug=post.slug)

            context = {'form': post_form}
            return render(request, 'hta_platform/create_post.html', context)


def view_post(request, *args, **kwargs):
    post_slug = kwargs.get("slug")

    try:
        post = Post.objects.get(slug=post_slug)
    except Post.DoesNotExist():
        return HttpResponse("Post doesn't exist")

    if post:
        context = {'post': post}
        return render(request, 'hta_platform/view_post.html', context)


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
                return redirect('view_post', slug=post.slug)
        context = {'form': post_form, 'post': post}
        return render(request, 'hta_platform/update_post.html', context)


@login_required
def delete_post(request, slug):
    Post.objects.filter(slug=slug).delete()
    return redirect('home')
