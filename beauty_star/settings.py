import os
from pathlib import Path

from celery.schedules import crontab
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = os.getenv('DEBUG') == 'True'

ALLOWED_HOSTS = ["*"]
CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1', 'http://localhost']

INSTALLED_APPS = [
    # GRAPPELLY ADMIN
    # "grappelli.dashboard",
    "grappelli",
    # DJANGO CONTRIB
    "django.contrib.sites",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django.contrib.sitemaps",
    "django_celery_beat",
    'main_site'
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

ROOT_URLCONF = 'beauty_star.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'main_site.context_processors.get_site_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'beauty_star.wsgi.application'

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.environ.get('DB_NAME'),
        "USER": os.environ.get('DB_USER'),
        "PASSWORD": os.environ.get('DB_PASSWORD'),
        "HOST": os.environ.get('DB_HOST'),
        "PORT": os.environ.get('DB_PORT'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True

USE_TZ = True

# STATIC
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATIC_ROOT = 'staticfiles'

# MEDIA
MEDIA_URL = 'media/'
MEDIA_DIRS = [
    BASE_DIR / 'media'
]
MEDIA_ROOT = 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SITE_ID = 1

ADMIN_TITLE = GRAPPELLI_ADMIN_TITLE = 'Завиток'

AUTH_USER_MODEL = 'main_site.User'

# BOT CONFIG
BOT_TOKEN = os.getenv('BOT_TOKEN')
TEST_TOKEN = os.getenv('TEST_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')


CELERY_PERIODICAL_TASKS = {
    "main_site": {
        "check_appointment_notification": {"schedule": crontab(minute="*/1")},
    },
}

BROKER_URL = "redis://0.0.0.0:6379/1"
CELERY_RESULT_BACKEND = "redis://0.0.0.0:6379/1"
CELERY_BROKER_URL = "redis://0.0.0.0:6379/2"
