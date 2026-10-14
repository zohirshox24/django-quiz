from django.core.management.base import BaseCommand
from quiz.models import Category, Question, Choice


class Command(BaseCommand):
    help = "Namuna kategoriya va savollarni bazaga qo'shadi"

    def handle(self, *args, **options):
        data = {
            "Python": [
                {
                    "text": "Python tilida ro'yxat (list) qaysi qavs bilan yoziladi?",
                    "difficulty": "easy",
                    "choices": [
                        ("[]", True),
                        ("{}", False),
                        ("()", False),
                        ("<>", False),
                    ],
                },
                {
                    "text": "Python'da funksiyani qaysi kalit so'z bilan e'lon qilamiz?",
                    "difficulty": "easy",
                    "choices": [
                        ("func", False),
                        ("def", True),
                        ("function", False),
                        ("lambda", False),
                    ],
                },
                {
                    "text": "Quyidagi kodlar ichida o'zgarmas (immutable) tur qaysi?",
                    "difficulty": "medium",
                    "choices": [
                        ("list", False),
                        ("dict", False),
                        ("tuple", True),
                        ("set", False),
                    ],
                },
                {
                    "text": "`len([1, 2, 3])` natijasi nechaga teng?",
                    "difficulty": "easy",
                    "choices": [
                        ("2", False),
                        ("3", True),
                        ("4", False),
                        ("Xato chiqadi", False),
                    ],
                },
                {
                    "text": "Python'da istisnolarni ushlash uchun qaysi blok ishlatiladi?",
                    "difficulty": "medium",
                    "choices": [
                        ("try / except", True),
                        ("catch / throw", False),
                        ("do / catch", False),
                        ("handle / error", False),
                    ],
                },
            ],
            "Django": [
                {
                    "text": "Django'da modelni bazaga qo'llash uchun qaysi buyruq ishlatiladi?",
                    "difficulty": "easy",
                    "choices": [
                        ("python manage.py migrate", True),
                        ("python manage.py start", False),
                        ("python manage.py build", False),
                        ("python manage.py update", False),
                    ],
                },
                {
                    "text": "Django'da URL yo'llarini qaysi faylda belgilaymiz?",
                    "difficulty": "easy",
                    "choices": [
                        ("models.py", False),
                        ("urls.py", True),
                        ("views.py", False),
                        ("settings.py", False),
                    ],
                },
                {
                    "text": "ForeignKey nima uchun ishlatiladi?",
                    "difficulty": "medium",
                    "choices": [
                        ("Matn saqlash uchun", False),
                        ("Bir modelni boshqasiga bog'lash uchun", True),
                        ("Rasm yuklash uchun", False),
                        ("Parol shifrlash uchun", False),
                    ],
                },
                {
                    "text": "Class-Based View'larda ro'yxat ko'rsatish uchun qaysi klass ishlatiladi?",
                    "difficulty": "medium",
                    "choices": [
                        ("DetailView", False),
                        ("ListView", True),
                        ("FormView", False),
                        ("TemplateView", False),
                    ],
                },
                {
                    "text": "Django ORM'da barcha obyektlarni olish uchun qaysi metod ishlatiladi?",
                    "difficulty": "easy",
                    "choices": [
                        ("Model.get_all()", False),
                        ("Model.objects.all()", True),
                        ("Model.find()", False),
                        ("Model.select()", False),
                    ],
                },
                {
                    "text": "`@login_required` dekoratori nima uchun ishlatiladi?",
                    "difficulty": "hard",
                    "choices": [
                        ("Sahifani tezlashtirish uchun", False),
                        ("Faqat tizimga kirgan foydalanuvchiga ruxsat berish uchun", True),
                        ("Xatolarni log qilish uchun", False),
                        ("Formani tekshirish uchun", False),
                    ],
                },
            ],
            "Ma'lumotlar bazasi": [
                {
                    "text": "SQL'da jadvaldan ma'lumot olish uchun qaysi buyruq ishlatiladi?",
                    "difficulty": "easy",
                    "choices": [
                        ("GET", False),
                        ("SELECT", True),
                        ("FETCH", False),
                        ("PULL", False),
                    ],
                },
                {
                    "text": "Bazada asosiy kalit (Primary Key) nima uchun kerak?",
                    "difficulty": "medium",
                    "choices": [
                        ("Jadvalni bezash uchun", False),
                        ("Har bir qatorni yagona aniqlash uchun", True),
                        ("Ma'lumotni shifrlash uchun", False),
                        ("Indeksni o'chirish uchun", False),
                    ],
                },
                {
                    "text": "Ikki jadvalni bog'lash uchun odatda qaysi kalit ishlatiladi?",
                    "difficulty": "medium",
                    "choices": [
                        ("Primary Key", False),
                        ("Foreign Key", True),
                        ("Unique Key", False),
                        ("Super Key", False),
                    ],
                },
                {
                    "text": "SQLite — bu qanday turdagi baza?",
                    "difficulty": "easy",
                    "choices": [
                        ("Fayl asosidagi yengil baza", True),
                        ("Faqat bulutli baza", False),
                        ("NoSQL baza", False),
                        ("Grafik baza", False),
                    ],
                },
                {
                    "text": "`ORDER BY` buyrug'i nima uchun ishlatiladi?",
                    "difficulty": "easy",
                    "choices": [
                        ("Jadval yaratish uchun", False),
                        ("Natijalarni tartiblash uchun", True),
                        ("Qator o'chirish uchun", False),
                        ("Ustun qo'shish uchun", False),
                    ],
                },
            ],
        }

        for category_name, questions in data.items():
            category, _ = Category.objects.get_or_create(name=category_name)
            self.stdout.write(self.style.SUCCESS(f"Kategoriya: {category_name}"))

            for q in questions:
                question, created = Question.objects.get_or_create(
                    category=category,
                    text=q["text"],
                    defaults={"difficulty": q["difficulty"]},
                )
                if created:
                    for choice_text, is_correct in q["choices"]:
                        Choice.objects.create(
                            question=question,
                            text=choice_text,
                            is_correct=is_correct,
                        )
                    self.stdout.write(f"  + {q['text'][:50]}")

        self.stdout.write(self.style.SUCCESS("Barcha savollar muvaffaqiyatli qo'shildi!"))