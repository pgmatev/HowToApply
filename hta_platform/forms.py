from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import University, Student


class AuthenticateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UniversityForm(forms.ModelForm):
    class Meta:
        model = University
        fields = ['name', 'website']

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['age']
