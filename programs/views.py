from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory

from .models import Program, ProgramExam
from hta_platform.models import User
from .forms import ProgramForm, ProgramExamForm


def list_programs(request, *args, **kwargs):
    university_username = kwargs.get("university_username")
    print(university_username)
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
    # ProgramExamFormset = modelformset_factory(ProgramExam, form=ProgramExamForm, extra=2)
    # formset = ProgramExamFormset() #TODO in create_program create only program,
                                   # have another view with formset for creating program exams
    # exams = user.university.exam_set.all()
    # for form in formset:
    #     form.fields['exam'].queryset = exams
    # print(exams)
    # program_exam_form = ProgramExamForm()
    # program_exam_form.fields['exam'].queryset = exams

    if user:
        if hasattr(user, 'university'):
            if request.method == 'POST':
                program_form = ProgramForm(request.POST)
                # formset = ProgramExamFormset(request.POST)

                # program_exam_form = ProgramExamForm(request.POST)
                # program_exam_form.fields['exam'].queryset = exams

                if program_form.is_valid():
                    program = program_form.save(commit=False)
                    program.university = user.university
                    # program_exam = program_exam_form.save(commit=False)
                    # program_exam.program = program
                    program.save()
                    # for form in formset:
                    #     program_exam = form.save(commit=False)
                    #     program_exam.program = program
                    #     program_exam.save()
                    return redirect('programs:view_program', university_username=user.username, program_id=program.id)

            context = {'program_form': program_form}
            return render(request, 'programs/create_program.html', context)


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