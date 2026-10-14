import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent


# --- Xavfsizlik ---
# Serverda kalit va DEBUG muhit o'zgaruvchilaridan olinadi (WSGI faylda beriladi).
# Kompyuteringizda o'zgaruvchilar yo'q, shuning uchun lokal qiymatlar ishlaydi.
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "django-insecure-faqat-lokal-uchun")
DEBUG = os.environ.get("DJANGO_DEBUG", "1") == "1"

if not DEBUG and SECRET_KEY.startswith("django-insecure"):
    raise ImproperlyConfigured(
        "Serverda DJANGO_SECRET_KEY muhit o'zgaruvchisini yangi kalit bilan bering."
    )

ALLOWED_HOSTS = ["zohirshox7.pythonanywhere.com", "localhost", "127.0.0.1"]
if DEBUG:
    # Lokal rejimda Wi-Fi orqali boshqalar ham kira olishi uchun
    ALLOWED_HOSTS.append("*")

CSRF_TRUSTED_ORIGINS = ["https://zohirshox7.pythonanywhere.com"]

if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True


# --- Ilovalar ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',

    'quiz',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# --- Ma'lumotlar bazasi ---
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# --- Parol tekshiruvlari ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# --- Til va vaqt ---
LANGUAGE_CODE = 'uz'
TIME_ZONE = 'Asia/Tashkent'
USE_I18N = True
USE_TZ = True


# --- Static fayllar ---
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'


# --- Login / Logout ---
LOGIN_URL = "quiz:login"
LOGIN_REDIRECT_URL = "quiz:home"
LOGOUT_REDIRECT_URL = "quiz:home"