from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('create-quiz/', views.create_quiz, name='create_quiz'),
    path('add-question/<int:quiz_id>/', views.add_question, name='add_question'),
    path('add-choice/<int:question_id>/', views.add_choice, name='add_choice'),
    path('quiz/<int:quiz_id>/', views.start_quiz, name='start_quiz'),
    path('dashboard/', views.dashboard, name='dashboard'),
]