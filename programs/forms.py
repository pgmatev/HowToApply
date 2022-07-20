from django import forms

from .models import Program, ProgramExam
from exams.models import Exam


class ProgramForm(forms.ModelForm):

    class Meta:
        model = Program
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Program name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'obligatory_coef': forms.NumberInput(
                attrs={'step': 0.01, 'class': 'form-control', 'placeholder': 'Coefficient of Obligatory Mark'}),
        }
        fields = ['name', 'description', 'obligatory_coef']


class ProgramExamForm(forms.ModelForm):
    # def __init__(self, exams, *args, **kwargs):
    #     # exams = kwargs.pop('exams')
    #     super(ProgramExamForm, self).__init__(*args, **kwargs)
    #     self.fields['exam'].queryset = exams

    exam = forms.ModelChoiceField(queryset=Exam.objects.none(), empty_label='None', required=False)
    coef = forms.NumberInput()

    class Meta:
        model = ProgramExam
        widgets = {
            'coef': forms.NumberInput(
                attrs={'step': 0.01, 'class': 'form-control', 'placeholder': 'Coefficient of Exam Mark'})
        }
        fields = ['exam', 'coef']
