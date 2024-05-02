from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from .models import Quiz, Question, Option
from .forms import QuizForm, QuestionForm, OptionFormSet
from django.http import HttpResponseRedirect

def login_view(request):
     if request.method == 'POST':
          form = AuthenticationForm(data=request.POST)  # Pass data argument here
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

def view_results(request):
    return render(request, 'view_results.html')

def add_question(request, quiz_title):
    quiz_form = QuizForm(initial={'title': quiz_title})
    question_form = QuestionForm()
    option_formset = OptionFormSet()

    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        option_formset = OptionFormSet(request.POST)
        if 'save_quiz' in request.POST:
                return render(request, 'my_quizzes')

        if question_form.is_valid() and option_formset.is_valid():
            selected_option = request.POST.get('correct_option')
            if not selected_option:
                return render(request, 'add_question')

            question = question_form.save(commit=False)
            question.quiz = Quiz.objects.get(title=quiz_title)
            question.save()

            for form in option_formset:
                option = form.save(commit=False)
                option.question = question
                option.is_correct = (form.cleaned_data['id'] == int(selected_option))
                option.save()
            return render(request, 'add_question')

    return render(request, 'add_question.html', {
        'quiz_title': quiz_title,
        'quiz_form': quiz_form,
        'question_form': question_form,
        'option_formset': option_formset,
    })

def create_quiz(request):
    if request.method == 'POST':
        quiz_title = request.POST.get('quiz_title')
        if quiz_title:
            return redirect('add_question', quiz_title=quiz_title)
    return render(request, 'create_quiz.html')

def my_quizzes(request):
    user = request.user
    quizzes = Quiz.objects.filter(user=user)

    return render(request, 'my_quizzes.html', {'quizzes': quizzes})
