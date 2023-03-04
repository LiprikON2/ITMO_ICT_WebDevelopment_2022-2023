"""
Django settings for Librarian project.

Generated by 'django-admin startproject' using Django 4.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-$g6nu3p_d7_eil3oz!@@&cx(1so^wz-3wh+tabgh=j^$s@a2c+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["localhost", '127.0.0.1', '192.168.1.246']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'drf_yasg',
    "phonenumber_field",
    'django_vite',

    'backend',
    'frontend',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Librarian.urls'

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
            'libraries':{
                'env_utils': 'frontend.templatetags.env_utils',
            }
        },
    },
]

WSGI_APPLICATION = 'Librarian.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# App specific settings
AUTH_USER_MODEL = "backend.User"

INTERNAL_IPS = [
    "localhost"
    "127.0.0.1",
    "192.168.1.246"
]

# Rest related
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAdminUser',
    ),
}


# Djoser related
DJOSER = {
    'SERIALIZERS': {
        'user': 'backend.serializers.UserSerializer',
    },
}


# Vite related

# Where ViteJS assets are built.
DJANGO_VITE_ASSETS_PATH = BASE_DIR / "frontend" / "static" / "dist"
# Whether to use HMR or not.
DJANGO_VITE_DEV_MODE = DEBUG


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

# Name of static files folder (named after `python manage.py collectstatic``)
STATIC_ROOT = BASE_DIR / "collectedstatic"

STATIC_URL = '/static/'

# Includes DJANGO_VITE_ASSETS_PATH into STATICFILES_DIRS to be copied
# when `python manage.py collectstatic` command is executed
STATICFILES_DIRS = [DJANGO_VITE_ASSETS_PATH]

# Enviroment variable `frontend_port` is set by `run.sh`
FRONTEND_PORT = os.environ.get("frontend_port", 3000)

DJANGO_VITE_DEV_SERVER_PORT = FRONTEND_PORT


# CORS related

CORS_ORIGIN_WHITELIST = [
    f'http://localhost:{FRONTEND_PORT}',
    f'http://127.0.0.1:{FRONTEND_PORT}',
    f'http://192.168.1.246:{FRONTEND_PORT}',
]
