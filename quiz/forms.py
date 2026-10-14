from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Question


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class QuizForm(forms.Form):
    """Kategoriya bo'yicha savollardan dinamik yasaladigan forma"""

    def __init__(self, category, *args, **kwargs):
        super().__init__(*args, **kwargs)
        questions = Question.objects.filter(category=category).prefetch_related("choices")

        for question in questions:
            choices = [(choice.id, choice.text) for choice in question.choices.all()]
            field = forms.ChoiceField(
                label=question.text,
                choices=choices,
                widget=forms.RadioSelect,
                required=True,
            )
            field.difficulty = question.difficulty
            self.fields[f"question_{question.id}"] = field