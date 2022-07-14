from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required

from .models import Program
from hta_platform.models import User
from .forms import ProgramForm, ProgramExamForm


def list_programs(request, *args, **kwargs):
    university_username = kwargs.get("university_username")

    try:
        user = User.objects.get(username=university_username)
    except User.DoesNotExist():
        return HttpResponse("User doesn't exist")

    programs = Program.objects.filter(university=user.university)
    context = {'university': user.university, 'programs': programs}
    return render(request, 'programs/list_programs.html', context)


def view_program(request, *args, **kwargs):
    program = kwargs.get("program_id")

    try:
        program = Program.objects.get(id=program)
    except Program.DoesNotExist():
        return HttpResponse("Post doesn't exist")

    if program:
        context = {'program': program}
        return render(request, 'programs/view_program.html', context)


@login_required
def create_program(request):
    user = request.user
    program_form = ProgramForm()
    exams = user.university.exam_set.all()
    print(exams)
    program_exam_form = ProgramExamForm()
    program_exam_form.fields['exam'].queryset = exams

    if user:
        if hasattr(user, 'university'):
            if request.method == 'POST':
                program_form = ProgramForm(request.POST)
                program_exam_form = ProgramExamForm(request.POST)
                program_exam_form.fields['exam'].queryset = exams

                if program_form.is_valid() & program_exam_form.is_valid():
                    program = program_form.save(commit=False)
                    program.university = user.university
                    program_exam = program_exam_form.save(commit=False)
                    program_exam.program = program
                    program.save()
                    program_exam.save()
                    return redirect('programs:view_program', university_username=user.username, program_id=program.id)

            context = {'program_form': program_form, 'program_exam_form': program_exam_form}
            return render(request, 'programs/create_program.html', context)
