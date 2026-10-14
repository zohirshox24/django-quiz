from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = "quiz"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("categories/", views.CategoryListView.as_view(), name="category_list"),
    path("quiz/<slug:slug>/", views.QuizView.as_view(), name="quiz"),
    path("result/<int:pk>/", views.ResultView.as_view(), name="result"),
    path("leaderboard/", views.LeaderboardView.as_view(), name="leaderboard"),

    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="quiz:home"), name="logout"),
]