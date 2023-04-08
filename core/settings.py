import os
from pathlib import Path

import sentry_sdk
from decouple import config  # type: ignore
from sentry_sdk.integrations.django import DjangoIntegration

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "8be1078ca645eb0545c5b71953075eef16347fea40d3a6fb"

DEBUG = config("DEBUG")

ALLOWED_HOSTS = []

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "django.contrib.sitemaps",  # django sitemap
    "django.contrib.sites",  # django sitemap enabled
    "tinymce",
]

API_APPS = [
    "api.apps.ApiConfig",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "rest_framework",
    "djoser"
    # "django_elasticsearch_dsl",
    # "social_django",
]

NAIJAPOINTER_APPS = [
    "accounts.apps.AccountsConfig",
    "news.apps.NewsConfig",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + NAIJAPOINTER_APPS + API_APPS

SITE_ID = 1

if DEBUG:
    INSTALLED_APPS += ["debug_toolbar"]
    # Debug settings
    INTERNAL_IPS = [
        "127.0.0.1",
    ]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    # debug middleware
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # 'social_django.middleware.SocialAuthExceptionMiddleware',  # social login with facebook
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # 'social_django.context_processors.backends',  # social
                # 'social_django.context_processors.login_redirect', #social
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

# AUTHENTICATION_BACKENDS = (
#     'social_core.backends.twitter.TwitterOAuth',
#     'social_core.backends.facebook.FacebookOAuth2',
#     'django.contrib.auth.backends.ModelBackend',
# )

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("NAME"),
        "USER": config("USER"),
        "HOST": config("HOST"),
        "PASSWORD": config("PASSWORD"),
        "PORT": config("PORT"),
    }
}

AUTH_USER_MODEL = "accounts.User"

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


LANGUAGE_CODE = "en-us"

TIME_ZONE = "Africa/Lagos"

USE_I18N = True

USE_TZ = True

LOGIN_REDIRECT_URL = ""

REST_FRAMEWORK = {
    "COERCE_DECIMAL_TO_STRING": False,
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    # 'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.IsAdmin']
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}


SIMPLE_JWT = {
   'AUTH_HEADER_TYPES': ('JWT',),
}

DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': '#/password/reset/confirm/{uid}/{token}',
    'USERNAME_RESET_CONFIRM_URL': '#/username/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL': '#/activate/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': True,
    'USER_CREATE_PASSWORD_RETYPE':True,
    'SERIALIZERS': {},
}


# drf spectacular API
SPECTACULAR_SETTINGS = {
    "TITLE": "Naijapointers API",
    "DESCRIPTION": "Nigerian based news and covering some parts of the world News API docs",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "DEFAULT_GENERATOR_CLASS": "drf_spectacular.generators.SchemaGenerator",
    'SWAGGER_UI_DIST': 'SIDECAR',  # shorthand to use the sidecar instead
    'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
    'REDOC_DIST': 'SIDECAR',
    'COMPONENT_SPLIT_REQUEST': True,
    'COMPONENT_NO_READ_ONLY_REQUIRED': True
}


STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "core/static")]

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

ELASTICSEARCH_DSL = {"default": {"hosts": "localhost:9200"}}


SOCIAL_AUTH_FACEBOOK_KEY = "1170503466932912"
SOCIAL_AUTH_FACEBOOK_SECRET = "95040e71ee3e6f61981e356760e02a5e"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# sentry error

sentry_sdk.init(
    dsn= config('DSN'),
    integrations=[
        DjangoIntegration(),
    ],
    traces_sample_rate=1.0,
    send_default_pii=True
)


# Logging errors
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'mainroot.log',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'level': os.environ.get('DJANGO_LOG_LEVEL','INFO')
        }
    },
    'formatters': {
        'verbose': {
            'format': '{asctime} ({levelname}) - {name} - {message}',
            'style': '{'
        }
    }
    
}
