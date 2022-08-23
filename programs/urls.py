from . import views
from django.urls import path

app_name = "programs"

urlpatterns = [
    path('list/<university_username>', views.list_programs, name='list_programs'),
    path('<program_id>', views.view_program, name='view_program'),
    path('<program_id>/edit', views.update_program, name='update_program'),
    path('create/', views.create_program, name='create_program'),
    path('create/<program_id>', views.create_program_exam, name='create_program_exam')
]
