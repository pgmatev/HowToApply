from . import views
from django.urls import path

app_name = "programs"

urlpatterns = [
    path('programs/<university_username>', views.list_programs, name='list_programs'),
    path('programs/<university_username>/<program_id>', views.view_program, name='view_program'),
    path('program/create', views.create_program, name='create_program')
]
