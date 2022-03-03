from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('university_register/', views.university_register, name='university_register'),
    path('register/', views.student_register, name='student_register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    # path('profile/', views.profile, name='profile'),
    path('search/', views.search, name='search'),
    path('profiles/<user_id>', views.profile, name='profiles'),
    path('create_post', views.create_post, name='create_post'),
    path('posts/<slug>', views.view_post, name='view_post'),
    path('posts/update/<slug>', views.update_post, name='update_post'),
    path('posts/delete/<slug>', views.delete_post, name='delete_post')
    # path('<university.username>')
]
