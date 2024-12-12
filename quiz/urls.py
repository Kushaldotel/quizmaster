from django.urls import path
from . import views

urlpatterns = [
    path('', views.select_category, name='select_category'),
    path('quiz/start/<int:category_id>/', views.start_quiz, name='start_quiz'),

    # URL for displaying 10 random questions (after starting the quiz)
    path('quiz/<int:category_id>/', views.display_question, name='display_question'),

    path('quiz/completed/<int:category_id>/<int:correct_answers>/<int:incorrect_answers>/', views.quiz_completed, name='quiz_completed'),


]
