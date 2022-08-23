from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory

from .models import Program, ProgramExam
from hta_platform.models import User
from .forms import ProgramForm, ProgramExamForm


def list_programs(request, *args, **kwargs):
    university_username = kwargs.get("university_username")
    try:
        user = User.objects.get(username=university_username)
    except User.DoesNotExist():
        return HttpResponse("User doesn't exist")

    programs = Program.objects.filter(university=user.university).order_by('name')

    program_letters = []
    for program in programs:
        if program.name[0] not in program_letters:
            program_letters.append(program.name[0])  # first letter of the programs so to form a dictionary
    context = {'university': user.university, 'programs': programs, 'program_letters': program_letters}
    return render(request, 'programs/list_programs.html', context)


def view_program(request, *args, **kwargs):
    program = kwargs.get("program_id")

    try:
        program = Program.objects.get(id=program)
    except Program.DoesNotExist():
        return HttpResponse("Post doesn't exist")

    if program:
        program_exams = ProgramExam.objects.filter(program=program)
        context = {'program': program, 'program_exams': program_exams}
        return render(request, 'programs/view_program.html', context)


@login_required
def create_program(request):
    user = request.user
    program_form = ProgramForm(request.POST or None)
    if user:
        if hasattr(user, 'university'):
            if request.method == 'POST':
                if program_form.is_valid():
                    program = program_form.save(commit=False)
                    program.university = user.university
                    program.save()

                    return redirect('programs:create_program_exam', program_id=program.id)

            context = {'program_form': program_form}
            return render(request, 'programs/create_program.html', context)


@login_required
def create_program_exam(request, *args, **kwargs):
    program_id = kwargs.get("program_id")
    program = Program.objects.get(id=program_id)

    user = request.user

    ProgramExamFormset = modelformset_factory(ProgramExam, form=ProgramExamForm)
    qs = program.programexam_set.all()
    formset = ProgramExamFormset(request.POST or None, queryset=qs)

    exams = user.university.exam_set.all()
    for form in formset:
        form.fields['exam'].queryset = exams

    if user:
        if hasattr(user, 'university'):
            if request.method == 'POST':
                if formset.is_valid():
                    for form in formset:
                        program_exam = form.save(commit=False)
                        program_exam.program = program
                        program_exam.save()

                return redirect('programs:view_program', program_id=program.id)

            context = {'formset': formset, 'program': program}
            return render(request, 'programs/create_program_exam.html', context)


@login_required
def update_program(request, *args, **kwargs):
    program_id = kwargs.get("program_id")
    user = request.user

    try:
        program = Program.objects.get(id=program_id)
    except Program.DoesNotExist():
        return HttpResponse("Post doesn't exist")

    if program and user == program.university.user:
        program_form = ProgramForm(instance=program)

        if request.method == 'POST':
            program_form = ProgramForm(request.POST, instance=program)

            if program_form.is_valid():
                program = program_form.save()
                return redirect('programs:view_program', id=program.id)
        context = {'form': program_form, 'program': program}
        return render(request, 'programs/update_program.html', context)