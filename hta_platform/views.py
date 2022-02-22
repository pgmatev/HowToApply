from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic.detail import DetailView

from .forms import UniversityForm, StudentForm, AuthenticateUserForm, AuthenticateUniversityForm
from .models import Student, University


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


# class StudentDetailView(DetailView):
#
#     model = Student
#     template_name = 'hta_platform/student_profile.html'
#
#     def get_context_data(self, **kwargs):
#         student = get_object_or_404(Student, id=self.kwargs['pk'])
#         current_user = request.user
#         context = super(StudentDetailView, self).get_context_data(**kwargs)
#         context['student'] = student
#         context['user'] = current_user
#         return context

def home(request):
    return render(request, 'hta_platform/home.html')


@login_required(login_url='/')
def profile(request):
    current_user = request.user

    if hasattr(current_user, 'student'):
        context = {'user': current_user, 'student': current_user.student}
        return render(request, 'hta_platform/student_profile.html', context)
    elif hasattr(current_user, 'university'):
        context = {'user': current_user, 'student': current_user.university}
        return render(request, 'hta_platform/university_profile.html', context)
    else:
        context = {'user': current_user}
        # need to pass message
        return render(request, 'hta_platform/home.html', context)


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
            # university.user.is_active = False
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
