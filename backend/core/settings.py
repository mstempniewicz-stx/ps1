"""Django settings for core project."""

import logging
import os
from datetime import timedelta

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# TODO: SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "I'M NOT SECRET UNLESS YOU CHANGE ME"  # TODO

INSTALLED_APPS = (
    "whitenoise.runserver_nostatic",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.admin",
    "raven.contrib.django.raven_compat",
    "rest_framework",
    "django_extensions",
    "health_check",  # required
    "health_check.db",  # stock Django health checkers
    "health_check.cache",
    "corsheaders",
    "base",
    "accounts",
    "celery",
)

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "corsheaders.middleware.CorsMiddleware",
]

ROOT_URLCONF = "core.urls"

WSGI_APPLICATION = "core.wsgi.application"

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

AUTH_USER_MODEL = "accounts.User"

ACCOUNT_ACTIVATION_DAYS = 7  # days

STATIC_URL = "/back_static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static_root")
STATICFILES_DIRS = []


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "accounts" "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

MEDIA_ROOT = os.path.join(BASE_DIR, "static_dist")

# store static files locally and serve with whitenoise
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ############# REST FRAMEWORK ###################

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": (),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_PARSER_CLASSES": (
        "djangorestframework_camel_case.parser.CamelCaseFormParser",
        "djangorestframework_camel_case.parser.CamelCaseMultiPartParser",
        "djangorestframework_camel_case.parser.CamelCaseJSONParser",
    ),
    "DEFAULT_RENDERER_CLASSES": (
        "djangorestframework_camel_case.render.CamelCaseJSONRenderer",
    ),
}

DEBUG = os.environ.get("DEBUG", "false").lower() == "true"
TEMPLATE_DEBUG = DEBUG
CORS_ORIGIN_ALLOW_ALL = DEBUG

REMOTE_STORAGE = (
    os.environ.get("REMOTE_FILE_STORAGE_ENABLED", "false").lower() == "true"
)
if REMOTE_STORAGE:
    AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
    AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
    AWS_STORAGE_BUCKET_NAME = os.environ["AWS_STORAGE_BUCKET_NAME"]
    AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
    AWS_REGION = os.environ["AWS_REGION"]
    AWS_S3_HOST = f"s3.{AWS_REGION}.amazonaws.com"
    AWS_DEFAULT_ACL = "private"
    AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto.S3BotoStorage"
    INSTALLED_APPS += ("health_check.contrib.s3boto_storage", "storages")
else:
    INSTALLED_APPS += ("health_check.storage",)
    logger.info("Using local file storage")

PAGE_CACHE_SECONDS = 60

# TODO: n a real production server this should have a proper url
ALLOWED_HOSTS = ["*"]

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME", "postgres"),
        "USER": os.environ.get("DB_USER", "postgres"),
        "PASSWORD": os.environ.get("DB_PASS", "postgres"),
        "HOST": os.environ.get("DB_HOST", "localhost"),
        "PORT": os.environ.get("DB_PORT", "5432"),
    }
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{os.environ.get('REDIS_URI', 'localhost:6379')}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "SOCKET_TIMEOUT": 900,
        },
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_FROM = os.environ.get("EMAIL_FROM")
FRONTEND_RESET_PASSWORD_URL = os.environ.get("FRONTEND_RESET_PASSWORD_URL")

# Celery configuration
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND")
CELERY_ACCEPT_CONTENT = ("application/json",)
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
