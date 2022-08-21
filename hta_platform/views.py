from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q

from .forms import UniversityForm, EditStudentForm, EditUserForm,\
                AuthenticateUserForm, AuthenticateUniversityForm
from .models import Student, University, User, StudentExam, Subject
from posts.models import Post
from programs.models import Program
from exams.models import Exam

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
            print(posts)
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


@login_required
def edit_profile(request):
    user = request.user

    if user:
        if hasattr(user, 'student'):
            edit_user_form = EditUserForm(instance=user)
            edit_student_form = EditStudentForm(instance=user.student)

            if request.method == 'POST':
                edit_user_form = EditUserForm(request.POST, instance=user)
                edit_student_form = EditStudentForm(request.POST, instance=user.student)

                if edit_user_form.is_valid() and edit_student_form.is_valid():
                    edit_student_form.full_clean()
                    user = edit_user_form.save()
                    user.student = edit_student_form.save()

                    return redirect(request, 'profiles', user.id)

            context = {'edit_user_form': edit_user_form, 'edit_student_form': edit_student_form, 'user': user}
            return render(request, 'hta_platform/edit_student_profile.html', context)
        elif hasattr(user, 'university'):
            # edit_user_form = EditUserForm(instance=user)
            # i need to decide which user attributes i want to edit in university edit and make a form for them
            edit_university_form = UniversityForm(instance=user.university)

            if request.method == 'POST':
                # edit_user_form = EditUserForm(request.POST, instance=user)
                edit_university_form = UniversityForm(request.POST, instance=user.university)

                if edit_university_form.is_valid():
                    edit_university_form.full_clean()
                    # user = edit_user_form.save()
                    user.university = edit_university_form.save()

                    return redirect('profiles', user.id)

            context = {'edit_university_form': edit_university_form, 'user': user}
            return render(request, 'hta_platform/edit_university_profile.html', context)
        else:
            context = {'user': user}
            # need to pass message
            return render(request, 'hta_platform/student_home.html', context)


@login_excluded('home')
def student_register(request):
    form = AuthenticateUserForm()

    if request.method == 'POST':
        form = AuthenticateUserForm(request.POST)

        if form.is_valid():
            user = form.save()
            student = Student.objects.create(user=user)
            student.save()
            return redirect('login')

    context = {'form': form}
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
            return redirect('hta_platform:login')

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
            return redirect('hta_platform:home')
        else:
            messages.info(request, 'Wrong credentials')

    return render(request, 'hta_platform/login.html')


@login_required
def logout_user(request):
    logout(request)
    return redirect('hta_platform:home')


def search(request):
    context = {}

    if request.method == 'GET':
        search_query = request.GET.get("q")
        if len(search_query) > 0:
            search_students = Student.objects.filter(Q(user__username__icontains=search_query) |
                                                     Q(user__email__icontains=search_query) |
                                                     Q(user__first_name__icontains=search_query) |
                                                     Q(user__last_name__icontains=search_query))
            search_universities = University.objects.filter(Q(user__username__icontains=search_query) |
                                                            Q(name__icontains=search_query))
            print("hi")
            search_programs = Program.objects.filter(Q(name__icontains=search_query) |
                                                        Q(description__icontains=search_query))
            print(search_programs)
            search_results = list(chain(search_students, search_universities))
            context['search_results'] = search_results
            context['search_query'] = search_query
            context['search_programs'] = search_programs

    return render(request, 'hta_platform/search_results.html', context)
