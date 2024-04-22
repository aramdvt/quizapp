from django.urls import path
from .views import login_view,register_view,success_view, explore_quizzes, create_quiz, view_results

urlpatterns = [
    path('', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('home/', success_view, name='home'),  
    path('explore/', explore_quizzes, name='explore_quizzes'),
    path('create/', create_quiz, name='create_quiz'),
    path('results/', view_results, name='view_results'),
]
