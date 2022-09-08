from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from hta_platform.models import User, Subject, Student
from .models import Exam, StudentExam
from .forms import ExamForm


def list_exams(request, *args, **kwargs):
    university_username = kwargs.get("university_username")
    try:
        user = User.objects.get(username=university_username)
    except User.DoesNotExist():
        return HttpResponse("User doesn't exist")
    if hasattr(user, "university"):
        exams = user.university.exam_set.all().order_by('name')
        exams_dict = {}
        for exam in exams:
            exams_dict.setdefault(exam.subject, []).append(exam)

        context = {'university': user.university, 'exams': exams_dict}
        return render(request, 'exams/list_exams.html', context)
    else:
        return HttpResponse("User is not a university")


@login_required
def create_exam(request):
    user = request.user
    exam_form = ExamForm(request.POST or None)

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


@login_required
def update_exam(request, *args, **kwargs):
    exam_id = kwargs.get("exam_id")
    user = request.user

    try:
        exam = Exam.objects.get(id=exam_id)
    except Exam.DoesNotExist():
        return HttpResponse("Post doesn't exist")

    if exam and user == exam.university.user:
        exam_form = ExamForm(request.POST or None, instance=exam)

        if request.method == 'POST':

            if exam_form.is_valid():
                exam = exam_form.save()
                return redirect('exams:view_exam', exam_id=exam.id)
        context = {'form': exam_form, 'exam': exam}
        return render(request, 'exams/update_exam.html', context)


@login_required
def delete_exam(request, exam_id):
    user = request.user

    try:
        exam = Exam.objects.get(id=exam_id)
    except Exam.DoesNotExist():
        return HttpResponse("Post doesn't exist")

    if exam and user == exam.university.user:
        exam.delete()

        return redirect('exams:list_exams', university_username=user.username)
    else:
        return redirect('exams:view_exam', exam_id=exam.id)


def view_exam(request, *args, **kwargs):
    exam_id = kwargs.get("exam_id")
    exam = Exam.objects.get(id=exam_id)

    user = request.user
    context = {'exam': exam}
    if user:
        if hasattr(user, "student"):
            student_exam = StudentExam.objects.get(student=user.student, exam=exam)
            if student_exam:
                print(student_exam.mark)
                context = {'exam': exam, 'is_registered': True, 'student_exam': student_exam}

        if hasattr(user, "university"):
            if exam.university == user.university:
                student_exams = list(StudentExam.objects.filter(exam=exam.id).order_by("student__user__first_name"))
                students_count = len(student_exams)
                if request.is_ajax() and request.method == 'POST':
                    if request.POST["action"] == "mark_student":
                        StudentExam.objects.filter(id=request.POST["student"]).update(mark=request.POST["mark"])
                    elif request.POST["action"] == "submit_marks":
                        exam.is_marked = True
                        exam.save()
                context = {'exam': exam, 'student_exams': student_exams,
                           'students_count': students_count}

    return render(request, 'exams/view_exam.html', context)


@login_required
def student_exam_register(request, *args, **kwargs):
    exam_id = kwargs.get("exam_id")
    user = request.user

    if hasattr(user, "student"):
        try:
            exam = Exam.objects.get(id=exam_id)
        except Exam.DoesNotExist():
            return HttpResponse("Exam doesn't exist")

        if not StudentExam.objects.filter(student=user.student, exam=exam).exists() and not exam.past_deadline:
            student_exam = StudentExam()
            student_exam.student = user.student
            student_exam.exam = exam
            student_exam.save()

        return redirect("exams:view_exam", exam_id=exam.id)


# @login_required
# def mark_student(request, *args, **kwargs)
#     exam_id = kwargs.get('exam_id')
#     student_id = kwargs.get('student_id')
#     user = request.user
#
#     if hasattr(user, 'university'):
#         try:
#             exam = Exam.objects.get(id=exam_id)
#             student = Student.objects.get(id=student_id)
#         except Exam.DoesNotExist() or Student.DoesNotExist():
#             return HttpResponse("Exam or Student don't exist")
#
#         if user.university == exam.university:
#             student_exam = StudentExam.objects.get(student=student, exam=exam)
#             if student_exam.exists():
#                 student_exam.mark = request.POST.get("mark")
