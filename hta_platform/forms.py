from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import University

class AuthenticateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1']

class UniversityForm(forms.ModelForm):
    class Meta:
        model = University
        fields = ['name', 'website']
