from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, FormView, DetailView, CreateView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from .models import Category, Question, UserScore
from .forms import QuizForm, RegisterForm


class HomeView(TemplateView):
    template_name = "quiz/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories_count"] = Category.objects.count()
        context["questions_count"] = Question.objects.count()
        context["players_count"] = UserScore.objects.values("user").distinct().count()
        return context


class CategoryListView(ListView):
    model = Category
    template_name = "quiz/category_list.html"
    context_object_name = "categories"


class QuizView(LoginRequiredMixin, FormView):
    template_name = "quiz/quiz.html"
    form_class = QuizForm

    def dispatch(self, request, *args, **kwargs):
        self.category = get_object_or_404(Category, slug=kwargs["slug"])
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["category"] = self.category
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        return context

    def form_valid(self, form):
        questions = Question.objects.filter(category=self.category).prefetch_related("choices")
        score = 0
        total = questions.count()
        details = []

        for question in questions:
            selected_id = form.cleaned_data.get(f"question_{question.id}")
            correct_choice = question.choices.filter(is_correct=True).first()
            selected_choice = question.choices.filter(id=selected_id).first()

            is_correct = bool(selected_choice and selected_choice.is_correct)
            if is_correct:
                score += 1

            details.append({
                "question": question.text,
                "selected": selected_choice.text if selected_choice else "Javob berilmagan",
                "correct": correct_choice.text if correct_choice else "",
                "is_correct": is_correct,
            })

        user_score = UserScore.objects.create(
            user=self.request.user,
            category=self.category,
            score=score,
            total_questions=total,
            details=details,
        )
        self.result_pk = user_score.pk
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("quiz:result", kwargs={"pk": self.result_pk})


class ResultView(LoginRequiredMixin, DetailView):
    model = UserScore
    template_name = "quiz/result.html"
    context_object_name = "result"

    def get_queryset(self):
        return UserScore.objects.filter(user=self.request.user)


class LeaderboardView(ListView):
    model = UserScore
    template_name = "quiz/leaderboard.html"
    context_object_name = "scores"
    ordering = ["-score"]
    paginate_by = 20


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "quiz/register.html"
    success_url = reverse_lazy("quiz:home")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class CustomLoginView(LoginView):
    template_name = "quiz/login.html"