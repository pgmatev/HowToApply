from . import views
from django.urls import path

app_name = 'exams'

urlpatterns = [
    path('list/<university_username>', views.list_exams, name='list_exams'),
    path('create/', views.create_exam, name='create_exam'),
    path('<exam_id>', views.view_exam, name='view_exam'),
    path('<exam_id>/update', views.update_exam, name='update_exam'),
    path('<exam_id>/delete', views.delete_exam, name='delete_exam'),
    path('<exam_id>/student_register', views.student_exam_register, name='student_exam_register')
]