from django import forms

from .models import Exam, StudentExam
from hta_platform.models import Subject


class ExamForm(forms.ModelForm):

    # exam_date: forms.DateTimeField()
    subject = forms.ModelChoiceField(queryset=Subject.objects.all(),
                                     widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Subject'}))

    class Meta:
        model = Exam
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'exam_date': forms.DateTimeInput(
                attrs={'class': 'form-control', 'type': 'datetime-local', 'placeholder': 'Exam Date'}),
            'deadline': forms.DateTimeInput(
                attrs={'class': 'form-control', 'type': 'datetime-local', 'placeholder': 'Registration deadline'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'})
        }
        fields = ['name', 'exam_date', 'deadline', 'subject', 'description']


class StudentExamForm(forms.ModelForm):
    class Meta:
        model = StudentExam
        widgets = {
            'mark': forms.NumberInput(
                attrs={'step': 0.01, 'class': 'form-control', 'placeholder': 'Mark'})
        }
        fields = ['mark']
