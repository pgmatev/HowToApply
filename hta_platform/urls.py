from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.universityRegister, name='university_register'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout')
]
