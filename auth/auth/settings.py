"""
Django settings for auth project.

Generated by 'django-admin startproject' using Django 2.2.24.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
from datetime import timedelta
from environ import Env

ENV = Env()
Env.read_env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ENV.str("SECRET_KEY", "debug-secret")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = ENV.bool("DEBUG", False)

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    # pre installed packages
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # custom packages
    "corsheaders",
    "rest_framework",
    "rest_framework_simplejwt",
    "drf_yasg",
    'django_filters',
    # Shoora modules
    "feature",
    "organization",
    "user",
    "device",
    "vehicle",
    "driver",
    "alert",
    "trip",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "auth.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "auth.wsgi.application"

# Rest Framework
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTStatelessUserAuthentication"
    ],
    "DEFAULT_PERMISSION_CLASSES": ["auth.permissions.AccessControlPermission"],
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend", "rest_framework.filters.OrderingFilter"],
    "DEFAULT_PAGINATION_CLASS": "auth.pagination.StandardResultsSetPagination",
    "PAGE_SIZE": 20,
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=8),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=180),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "uuid",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
}

# CORS
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

is_local_development = ENV.bool("LOCAL_DB", False)
if is_local_development:
    # Database
    # https://docs.djangoproject.com/en/2.2/ref/settings/#databases

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": ENV.str("DB_NAME", None),
            "USER": ENV.str("DB_USER", None),
            "PASSWORD": ENV.str("DB_PASSWORD", None),
            "HOST": ENV.str("DB_HOST", None),
            "PORT": ENV.str("DB_PORT", None),
        }
    }


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

# STATIC_URL = '/static/'

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIR = (os.path.join(BASE_DIR, "static"),)

# CELERY_BROKER_URL = "redis://redis:6379"
# CELERY_RESULT_BACKEND = "redis://redis:6379"
# CELERY_ACCEPT_CONTENT = ["application/json"]
# CELERY_TASK_SERIALIZER = "json"
# CELERY_RESULT_SERIALIZER = "json"

# AWS Credentials
AWS_ACCESS_KEY_ID = ENV.str('AWS_ACCESS_KEY_ID', None)
AWS_SECRET_ACCESS_KEY = ENV.str('AWS_SECRET_ACCESS_KEY', None)
# Celery
CELERY_BROKER_URL = "sqs://{aws_access_key}:{aws_secret_key}@".format(aws_access_key=AWS_ACCESS_KEY_ID, aws_secret_key=AWS_SECRET_ACCESS_KEY)
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_DEFAULT_QUEUE = 'video-telematics'
CELERY_RESULT_BACKEND = None # Disabling the results backend
BROKER_TRANSPORT_OPTIONS = {
    'region': 'ap-south-1',
    'polling_interval': 20,
}


from celery.schedules import crontab


celery_beat = ENV.str('celery_beat', False)
if celery_beat:
    CELERY_BEAT_SCHEDULE = {
        # 'hello': {
        #     'task': 'alert.tasks.hello',
        #     'schedule': crontab()  # execute every minute
        # },
        'alert':{
            'task': 'alert.tasks.fetch_alerts',
            'schedule': crontab(minute='*/10')  # execute every minute
        },
        'trip':{
            'task': 'trip.tasks.calculate_trips',
            'schedule': crontab(minute='*/10')  # execute every minute
        },
        # 'position':{
        #     'task': 'alert.tasks.poll_task',
        #     'schedule': 10.0  # execute every minute
        # }
    }

# China Server URLs
JSESSION_URL = ENV.str("JSESSION_URL", None)
FETCH_ALARM_VIDEO_URL = ENV.str("FETCH_ALARM_VIDEO_URL", None)

print(JSESSION_URL)

AUTH_USER_MODEL = "user.User"
