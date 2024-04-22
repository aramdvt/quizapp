from django import forms
from .models import Quiz, Question, Option

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title'] 

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']  

OptionFormSet = forms.inlineformset_factory(
    Question, Option, fields=('text', 'is_correct'), extra=2, max_num=5
)