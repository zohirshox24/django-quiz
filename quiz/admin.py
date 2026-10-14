from django.contrib import admin
from .models import Category, Question, Choice, UserScore


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "questions_count")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("text", "category", "difficulty")
    list_filter = ("category", "difficulty")
    inlines = [ChoiceInline]


@admin.register(UserScore)
class UserScoreAdmin(admin.ModelAdmin):
    list_display = ("user", "category", "score", "total_questions", "completed_at")
    list_filter = ("category",)