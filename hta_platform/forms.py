from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import University, Student


class AuthenticateUserForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
                    attrs={'class': 'form-control',
                           'type': 'password',
                           'placeholder': 'Password'}),
    )
    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(
                    attrs={'class': 'form-control',
                           'type': 'password',
                           'placeholder': 'Confirm Password'}),
    )

    class Meta:
        model = User
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class AuthenticateUniversityForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
                    attrs={'class': 'form-control',
                           'type': 'password',
                           'placeholder': 'Password'}),
    )
    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(
                    attrs={'class': 'form-control',
                           'type': 'password',
                           'placeholder': 'Confirm Password'}),
    )

    class Meta:
        model = User
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
        }
        fields = ['username', 'password1', 'password2']


class UniversityForm(forms.ModelForm):
    class Meta:
        model = University
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'University Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'University Description'}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Website Link'})
        }
        fields = ['name', 'description', 'website']


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }
        fields = ['username', 'first_name', 'last_name', 'email']


class EditStudentForm(forms.ModelForm):
    class Meta:
        model = Student
        widgets = {
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Age'}),
            'obligatory_mark': forms.NumberInput(
                attrs={'step': 0.01, 'class': 'form-control', 'placeholder': 'Obligatory Mark'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Bio'}),
        }
        fields = ['age', 'obligatory_mark', 'bio']
