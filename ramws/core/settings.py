import datetime as dt
import os
import sys

import dj_database_url
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# Build paths inside the project like this: os.path.join(BASE_DIR, ...).
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


##############
# ADMIN SITE #
##############

PROJECT_NAME = os.environ.get("PROJECT_NAME")
MAIN_SITE_URL = os.environ.get("MAIN_SITE_URL")


##########################
# APPLICATION DEFINITION #
##########################

BUILT_IN_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "corsheaders",
    "whitenoise.runserver_nostatic",
    "django_extensions",
]

FIRST_PARTY_APPS = [
    "accounts.apps.Config",
    "docs.apps.Config",
    "files.apps.Config",
]

INSTALLED_APPS = BUILT_IN_APPS + THIRD_PARTY_APPS + FIRST_PARTY_APPS


##################
# AUTHENTICATION #
##################

AUTH_USER_MODEL = "accounts.User"

SLIDING_TOKEN_LIFETIME = os.environ.get("SLIDING_TOKEN_LIFETIME", 365)
JWT_SIGNING_KEY = os.environ.get("JWT_SIGNING_KEY")
JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM")

SIMPLE_JWT = {
    "SLIDING_TOKEN_LIFETIME": dt.timedelta(days=SLIDING_TOKEN_LIFETIME),
    "SIGNING_KEY": JWT_SIGNING_KEY,
    "ALGORITHM": JWT_ALGORITHM,
    "AUTH_TOKEN_CLASSES": ["rest_framework_simplejwt.tokens.SlidingToken"],
}


#####################
# COMMON MIDDLEWARE #
#####################

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "core.middleware.CommonMiddleware",
    "django.middleware.common.BrokenLinkEmailsMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


########
# CORS #
########

CORS_ORIGIN_ALLOW_ALL = True


#############
# DATABASES #
#############

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DATABASE_NAME"),
        "USER": os.environ.get("DATABASE_USER"),
        "PASSWORD": os.environ.get("DATABASE_PASSWORD"),
        "HOST": os.environ.get("DATABASE_HOST"),
        "PORT": os.environ.get("DATABASE_PORT"),
    }
}

if "DATABASE_URL" in os.environ:
    DATABASES["default"] = dj_database_url.config(ssl_require=True)


###############
# ENVIRONMENT #
###############

TEST = "test" in sys.argv
DJANGO_ENV = os.environ.get("RUN_ENV")
DEBUG = DJANGO_ENV == "development"

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(" ")
ALLOWED_HEALTH_CHECK_USER_AGENTS = os.environ.get(
    "ALLOWED_HEALTH_CHECK_USER_AGENTS", ""
).split(" ")


##################
# HTML TEMPLATES #
##################

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "core", "templates")],
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


########################
# INTERNATIONALIZATION #
########################

LANGUAGE_CODE = "es-CL"
USE_I18N = True
USE_L10N = True


########
# LOGS #
########

PROPAGATE_EXCEPTIONS = True
DEFAULT_LOGGING_LEVEL = "INFO" if DEBUG else "WARNING"
LOGGING_LEVEL = os.environ.get("LOGGING_LEVEL", DEFAULT_LOGGING_LEVEL)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
        "null": {
            "class": "logging.NullHandler",
        },
    },
    "loggers": {
        "django.security.DisallowedHost": {
            "handlers": ["null"],
            "level": "CRITICAL",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": LOGGING_LEVEL,
    },
}


##################
# REST FRAMEWORK #
##################

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
}


###########
# SECRETS #
###########

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

AWS_REGION = os.environ.get("AWS_REGION")
RUNS_S3_BUCKET = os.environ.get("RUNS_S3_BUCKET")
RUNS_SQS_QUEUE = os.environ.get("RUNS_SQS_QUEUE")

AWS_LOCATION = os.environ.get("AWS_LOCATION", "")


##########
# SENTRY #
##########

SENTRY_DSN = os.environ.get("SENTRY_DSN")

sentry_sdk.init(
    dsn=SENTRY_DSN, integrations=[DjangoIntegration()], environment=DJANGO_ENV
)


################
# STATIC FILES #
################

STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")


############
# TIMEZONE #
############

USE_TZ = True
TIME_ZONE = "America/Santiago"


########
# URLS #
########

ROOT_URLCONF = "core.urls"
APPEND_SLASH = False


########
# WSGI #
########

WSGI_APPLICATION = "core.wsgi.application"
