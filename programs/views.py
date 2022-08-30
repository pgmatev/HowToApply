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

                    return redirect('programs:add_exam', program_id=program.id)

            context = {'program_form': program_form}
            return render(request, 'programs/create_program.html', context)


@login_required
def add_exam(request, *args, **kwargs):
    program_id = kwargs.get("program_id")
    program = Program.objects.get(id=program_id)

    user = request.user
    exams = user.university.exam_set.all()

    program_exam_formset = modelformset_factory(ProgramExam, form=ProgramExamForm, extra=1, can_delete=True)
    qs = program.programexam_set.all()
    formset = program_exam_formset(request.POST or None, queryset=qs)

    for form in formset:
        form.fields['exam'].queryset = exams

    if user:
        if hasattr(user, 'university'):
            if request.method == 'POST':
                if formset.is_valid():
                    for form in formset:
                        if form.is_valid() and form.has_changed():
                            if form.cleaned_data['DELETE']:
                                form.cleaned_data['id'].delete()
                            else:
                                program_exam = form.save(commit=False)
                                program_exam.program = program
                                program_exam.save()

                    return redirect('programs:view_program', program_id=program.id)

            context = {'formset': formset, 'program': program}
            return render(request, 'programs/add_exam.html', context)
# @login_required
# def add_exam(request, *args, **kwargs):
#     program_id = kwargs.get("program_id")
#     program = Program.objects.get(id=program_id)
#
#     user = request.user
#     exams = user.university.exam_set.all()
#
#     program_exam_form = ProgramExamForm(request.POST or None)
#     program_exam_form.fields['exam'].queryset = exams
#
#     if user:
#         if hasattr(user, 'university'):
#             if request.method == 'POST':
#                 if program_exam_form.is_valid():
#                     program_exam = program_exam_form.save(commit=False)
#                     program_exam.program = program
#                     program_exam.save()
#
#                     return redirect('programs:view_program', program_id=program.id)
#
#             context = {'program_exam_form': program_exam_form, 'program': program}
#             return render(request, 'programs/add_exam.html', context)


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
                return redirect('programs:add_exam', program_id=program.id)
        context = {'form': program_form, 'program': program}
        return render(request, 'programs/update_program.html', context)


@login_required
def delete_program(request, *args, **kwargs):
    program_id = kwargs.get("program_id")
    Program.objects.filter(id=program_id).delete()
    return redirect('programs:list_programs', university_username=request.user.username)