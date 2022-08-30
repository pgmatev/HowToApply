from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from hta_platform.models import User, Subject
from .models import Exam
from .forms import ExamForm


def list_exams(request, *args, **kwargs):
    university_username = kwargs.get("university_username")
    try:
        user = User.objects.get(username=university_username)
    except User.DoesNotExist():
        return HttpResponse("User doesn't exist")
    if hasattr(user, "university"):
        exams = user.university.exam_set.all()
        subjects = []
        for exam in exams:
            if exam.subject not in subjects:
                subjects.append(exam.subject)

        context = {'university': user.university, 'exams': exams, 'subjects': subjects}
        return render(request, 'exams/list_exams.html', context)
    else:
        return HttpResponse("User is not a university")


@login_required
def create_exam(request):
    user = request.user
    exam_form = ExamForm(request.POST or None)
    print(exam_form)

    if user:
        if hasattr(user, 'university'):
            if request.method == 'POST':
                if exam_form.is_valid():
                    exam = exam_form.save(commit=False)
                    exam.university = user.university
                    exam.save()

                    return redirect('exams:view_exam', exam_id=exam.id)

            context = {'exam_form': exam_form}
            return render(request, 'exams/create_exam.html', context)


def view_exam(request, *args, **kwargs):
    exam_id = kwargs.get("exam_id")
    exam = Exam.objects.get(id=exam_id)

    context = {'exam': exam}
    return render(request, 'exams/view_exam.html', context)