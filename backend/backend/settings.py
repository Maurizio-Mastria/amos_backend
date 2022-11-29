"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
# CoreRoot/settings.py

import environ
from pathlib import Path
from os.path import join
import os
# Initialise environment variables
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR,"..","..",".env"))

SECRET_KEY = env('SECRET_KEY', default='qkl+xdr8aimpf-&x(mi7)dwt^-q77aji#j*d#02-5usa32r9!y')
DEBUG = int(env("DEBUG", default=1))
ALLOWED_HOSTS = env("DJANGO_ALLOWED_HOSTS").split(" ")
BASE_URL=env("BASE_URL")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
DISK_A_PATH = env("DISK_A_PATH")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    #'backend.apps.CustomAdminConfig',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'django_otp',
    'django_otp.plugins.otp_totp',
    'phonenumber_field',
    'django_crontab',
    'profiles',
    'authentications',
    'companies',
    'marketplaces',
    'products',
    'offers',
    'messages.apps.MessagesConfig',
    'shippings',
    'orders',
    'daphne',
    'customers',
    'buckets',
    'imports',
    'stocks'
    
    
]

#CORS_ALLOWED_ORIGINS = env("CORS_ALLOWED_ORIGINS").split(" ")

CORS_ORIGIN_ALLOW_ALL=True

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]

}

CRONJOBS =[
    ('* * * * *', 'imports.cron.imports_job','>> imports.log'),
    ('* * * * *', 'imports.cron.process_imports_job','>> process_imports.log'),
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_otp.middleware.OTPMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [join(BASE_DIR,'templates'),],
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

TEMPLATE_DIR=join(BASE_DIR,'templates')


WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     },
# }
DATABASES = {
    'default': {
        'ENGINE': env('DB_ENGINE', default='django.db.backends.postgresql_psycopg2'),
        'NAME': env('DB_NAME', default='amosdb'),
        'USER': env('DB_USER', default='amos'),
        'PASSWORD': env('DB_PASSWORD', default='12345678'),
        'HOST': env('DB_HOST', default='localhost'),
        'PORT': env('DB_PORT', default='5432'),
    }
}



# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'it-it'

TIME_ZONE = 'Europe/Rome'

USE_I18N = True

USE_L10N = True

USE_TZ = True

FILE_UPLOAD_HANDLERS=[
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
]
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = env("STATIC_ROOT")
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


AUTO_LOGOUT_DELAY = 60*8 #equivalent to 5 minutes

APPEND_SLASH=False
MEDIA_URL = '/media/'
MEDIA_ROOT = join(BASE_DIR,'..','httpdocs','media')

DATA_UPLOAD_MAX_MEMORY_SIZE=5000000
#FILE_UPLOAD_TEMP_DIR=join(DISK_A_PATH,"tmp")
PUBLIC_DIR=os.path.join(DISK_A_PATH,"share")
PRIVATE_DIR=os.path.join(DISK_A_PATH,"private")
EMAIL_HOST=env("EMAIL_HOST")
EMAIL_PORT=env("EMAIL_PORT")
EMAIL_HOST_USER=env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD=env("EMAIL_HOST_PASSWORD")
EMAIL_USE_SSL=env("EMAIL_USE_SSL")
FILE_PATH_FIELD_DIRECTORY=PRIVATE_DIR