from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('university-register/', views.university_register, name='university_register'),
    path('register/', views.student_register, name='student_register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    # path('profile/', views.profile, name='profile'),
    path('search/', views.search, name='search'),
    path('profiles/<user_id>', views.profile, name='profiles'),
    path('profile/edit', views.edit_profile, name='edit_profile'),

    path('programs/<university_username>', views.list_programs, name='list_programs'),
    path('programs/<university_username>/<program_id>', views.view_program, name='view_program'),
    path('program/create', views.create_program, name='create_program')
    # path('<university.username>')
]
