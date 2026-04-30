from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-3dprint-md-change-in-production-xyz123abc'
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'shop',
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

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = []
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Chisinau'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ============================================================
# НАСТРОЙКИ EMAIL (заполни своими данными)
# ============================================================

# Твой email куда будут приходить уведомления о заказах
ORDER_NOTIFICATION_EMAIL = '3dprintmd@gmail.com'  # ← ЗАМЕНИ НА СВОЙ

# --- Вариант 1: Gmail ---
# Зайди в Google → Аккаунт → Безопасность → Двухэтапная аутентификация (включи)
# Потом: Аккаунт → Безопасность → Пароли приложений → Создай пароль для "Почта"
EMAIL_BACKEND   = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST      = 'smtp.gmail.com'
EMAIL_PORT      = 587
EMAIL_USE_TLS   = True
EMAIL_HOST_USER = 'malchickboy37@gmail.com'      # ← ЗАМЕНИ на свой Gmail
EMAIL_HOST_PASSWORD = 'wctg gqjz vlsj ifkx'  # ← пароль приложения (16 символов)
DEFAULT_FROM_EMAIL = 'malchickboy37@gmail.com'   # ← тот же Gmail

# --- Вариант 2: если хочешь пока просто видеть письма в консоли (для теста) ---
# Закомментируй всё выше и раскомментируй строку ниже:
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
