from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from .models import Quiz, Question, Option
from .forms import QuizForm, QuestionForm, OptionFormSet



def login_view(request):
     if request.method == 'POST':
          form = AuthenticationForm(request, request.POST)
          if form.is_valid():
               username = form.cleaned_data.get('username')
               password = form.cleaned_data.get('password')
               user = authenticate(username=username, password=password)
               if user is not None:
                    login(request, user)
                    return redirect('home')
     else:
        form = AuthenticationForm()
     return render(request, 'login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def success_view(request):
    return render(request, 'success.html', {'username': request.user.username})

def explore_quizzes(request):
    return render(request, 'explore_quizzes.html')

def create_quiz(request):
    return render(request, 'create_quiz.html')

def view_results(request):
    return render(request, 'view_results.html')


def create_quiz(request):
    if request.method == 'POST':
        quiz_form = QuizForm(request.POST)
        question_form = QuestionForm(request.POST)
        option_formset = OptionFormSet(request.POST)

        if quiz_form.is_valid() and question_form.is_valid() and option_formset.is_valid():
            quiz = quiz_form.save()
            question = question_form.save(commit=False)
            question.quiz = quiz
            question.save()
            option_formset.instance = question
            option_formset.save()
            return redirect('create_quiz')  
    else:
        quiz_form = QuizForm()
        question_form = QuestionForm()
        option_formset = OptionFormSet()
    
    return render(request, 'create_quiz.html', {
        'quiz_form': quiz_form,
        'question_form': question_form,
        'option_formset': option_formset,
    })
