from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Category(models.Model):
    """Viktorina yo'nalishi (masalan: Python, Django, Database)"""
    name = models.CharField(max_length=100, verbose_name="Nomi")
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def questions_count(self):
        return self.questions.count()


class Question(models.Model):
    """Savol"""
    DIFFICULTY_CHOICES = [
        ("easy", "Oson"),
        ("medium", "O'rta"),
        ("hard", "Qiyin"),
    ]

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="questions", verbose_name="Kategoriya")
    text = models.CharField(max_length=300, verbose_name="Savol matni")
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default="easy", verbose_name="Qiyinligi")

    class Meta:
        verbose_name = "Savol"
        verbose_name_plural = "Savollar"

    def __str__(self):
        return self.text


class Choice(models.Model):
    """Savol javob varianti"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices", verbose_name="Savol")
    text = models.CharField(max_length=200, verbose_name="Variant matni")
    is_correct = models.BooleanField(default=False, verbose_name="To'g'ri javobmi")

    class Meta:
        verbose_name = "Variant"
        verbose_name_plural = "Variantlar"

    def __str__(self):
        return self.text


class UserScore(models.Model):
    """Foydalanuvchi natijasi"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="scores", verbose_name="Foydalanuvchi")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="scores", null=True, blank=True, verbose_name="Kategoriya")
    score = models.PositiveIntegerField(default=0, verbose_name="To'plagan ball")
    total_questions = models.PositiveIntegerField(default=0, verbose_name="Jami savollar")
    details = models.JSONField(default=list, blank=True, verbose_name="Javoblar tafsiloti")
    completed_at = models.DateTimeField(auto_now_add=True, verbose_name="Vaqti")

    class Meta:
        verbose_name = "Natija"
        verbose_name_plural = "Natijalar"
        ordering = ["-score", "completed_at"]

    def __str__(self):
        return f"{self.user.username} - {self.score}/{self.total_questions}"

    @property
    def percent(self):
        if self.total_questions == 0:
            return 0
        return round(self.score / self.total_questions * 100)