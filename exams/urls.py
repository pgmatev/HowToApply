from . import views
from django.urls import path

app_name = 'exams'

urlpatterns = [
    path('list/<university_username>', views.list_exams, name='list_programs'),
    path('create/', views.create_exam, name='create_exam'),
    path('<exam_id>', views.view_exam, name='view_exam'),
]