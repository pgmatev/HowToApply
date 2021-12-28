from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UniversityForm, StudentForm, AuthenticateUserForm


# Create your views here.

def home(request):
    return render(request, 'hta_platform/home.html')


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


def university_register(request):
    form = UserCreationForm()
    university_form = UniversityForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        university_form = UniversityForm(request.POST)

        if form.is_valid() and university_form.is_valid():
            user = form.save()
            university = university_form.save(commit=False)
            university.user = user
            university.save()
            # messages.success(request, 'Successfully added ' + university_form.cleaned_data.get('username'))
            return redirect('login')

    context = {'form': form, 'university_form': university_form}
    return render(request, 'hta_platform/university_register.html', context)


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


def logout_user(request):
    logout(request)
    return redirect('login')