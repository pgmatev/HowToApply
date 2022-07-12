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
    path('post/create', views.create_post, name='create_post'),
    path('posts/<slug>', views.view_post, name='view_post'),
    path('post/update/<slug>', views.update_post, name='update_post'),
    path('post/delete/<slug>', views.delete_post, name='delete_post'),
    path('programs/<university_username>', views.list_programs, name='list_programs'),
    path('programs/<university_username>/<program_id>', views.view_program, name='view_program')
    # path('<university.username>')
]
