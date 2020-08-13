import os

import dj_database_url
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.rq import RqIntegration

from .aws import get_ecs_task_ips


IS_LTI = bool(os.environ.get("IS_LTI"))

# Initialize Sentry for Error Tracking (see also: https://docs.sentry.io/)
if not IS_LTI:
    sentry_sdk.init(
        dsn=os.environ.get("SENTRY_DSN"),
        debug=os.environ.get("SENTRY_DEBUG") == "1",
        environment=os.environ.get("SENTRY_ENVIRONMENT"),
        integrations=[DjangoIntegration(), RqIntegration()],
        # Enables tracing for sentry "Events V2"
        # https://github.com/getsentry/zeus/blob/764df526f47d9387a03b5afcdf3ec0758ae38ac2/zeus/config.py#L380
        traces_sample_rate=1.0,
        traceparent_v2=True,
    )

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
PACKAGE_ROOT = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = PACKAGE_ROOT

try:
    DEBUG = bool(int(os.environ.get("DJANGO_DEBUG", "1")))
except ValueError:
    DEBUG = False

DATABASES = {
    "default": dj_database_url.config(default="postgres://localhost/hedera")
}

CSRF_TRUSTED_ORIGINS = ["canvas.harvard.edu"]

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "hederaproject.org",
    ".hederaproject.org",
]

ALLOWED_HOSTS += get_ecs_task_ips()

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = "UTC"

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "en-us"

SITE_ID = int(os.environ.get("SITE_ID", 1))

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

USE_S3 = os.environ.get("USE_S3", False)
if USE_S3:
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
    AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME", "")
    AWS_DEFAULT_ACL = None
    AWS_S3_CUSTOM_DOMAIN = "s3.amazonaws.com/%s" % AWS_STORAGE_BUCKET_NAME
    AWS_S3_OBJECT_PARAMETERS = {
        "CacheControl": "max-age=86400",
    }
    STATICFILES_LOCATION = "static"
    STATICFILES_STORAGE = "hedera.custom_storages.StaticStorage"
    STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)
    MEDIAFILES_LOCATION = "media"
    DEFAULT_FILE_STORAGE = "hedera.custom_storages.MediaStorage"
    MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)
else:
    # URL that handles the media served from MEDIA_ROOT. Make sure to use a
    # trailing slash.
    # Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
    MEDIA_URL = "/media/"
    # URL prefix for static files.
    # Example: "http://media.lawrence.com/static/"
    STATIC_URL = "/static/"

    STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

    # Absolute filesystem path to the directory that will hold user-uploaded files.
    # Example: "/home/media/media.lawrence.com/media/"
    MEDIA_ROOT = os.path.join(PACKAGE_ROOT, "site_media", "media")
    # Absolute path to the directory static files should be collected to.
    # Don"t put anything in this directory yourself; store your static files
    # in apps" "static/" subdirectories and in STATICFILES_DIRS.
    # Example: "/home/media/media.lawrence.com/static/"
    STATIC_ROOT = os.path.join(PACKAGE_ROOT, "site_media", "static")
# Additional locations of static files
STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, "static", "dist"),
]

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# Make this unique, and don"t share it with anybody.
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "secretkey")

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(PACKAGE_ROOT, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "debug": DEBUG,
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.template.context_processors.request",
                "django.contrib.messages.context_processors.messages",
                "hedera.context_processors.settings",
                "account.context_processors.account",
            ],
        },
    },
]

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "querycount.middleware.QueryCountMiddleware",
    "hedera.middleware.AuthenticatedMiddleware",
]

AUTHENTICATED_EXEMPT_URLS = [
    "/favicon.ico",
    "/account/login/",
    "/account/signup/",
    "/account/password/reset/",
    "/account/confirm_email/",
    r"^/\.well-known/",
    "^/$",
    r"/api/",
    "/lti/lti_registration",
]

ROOT_URLCONF = "hedera.urls"

# Python dotted path to the WSGI application used by Django"s runserver.
WSGI_APPLICATION = "hedera.wsgi.application"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.flatpages",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.staticfiles",

    "webpack_loader",
    "storages",

    # templates
    "bootstrapform",
    "pinax.templates",

    # external
    "account",
    "pinax.eventlog",
    "django_rq",
    "lti_provider",

    # local apps
    "databasetext",
    "vocab_list",
    "lattices",
    "lemmatization",
    "lemmatized_text",
    "groups",
    "lti",

    # project
    "hedera",
]

if DEBUG:
    INSTALLED_APPS.append("sslserver")

RQ_ASYNC = bool(int(os.environ.get("RQ_ASYNC", "0")))
RQ_DATABASE = 1
RQ_QUEUES = {
    "default": {
        "URL": os.getenv("REDIS_URL", "redis://localhost:6379/"),
        "DB": RQ_DATABASE,
        "ASYNC": RQ_ASYNC
    }
}
RQ_SHOW_ADMIN_LINK = True

WEBPACK_LOADER = {
    "DEFAULT": {
        "CACHE": not DEBUG,
        "BUNDLE_DIR_NAME": "/",
        "STATS_FILE": os.path.join(PROJECT_ROOT, "webpack-stats.json"),
        "POLL_INTERVAL": 0.1,
        "TIMEOUT": None,
        "IGNORE": [r".*\.hot-update.js", r".+\.map"]
    }
}

ADMIN_URL = "admin:index"
CONTACT_EMAIL = "atg@fas.harvard.edu"

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
_DEFAULT_LOG_LEVEL = os.environ.get("LOG_LEVEL", "ERROR")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler"
        }
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": _DEFAULT_LOG_LEVEL,
        },
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
        "rq.worker": {
            "level": "DEBUG",
            "handlers": ["console"],
            "propagate": False,
        },
        "lemmatization": {
            "level": "DEBUG",
            "handlers": ["console"],
            "propagate": False
        }
    }
}

FIXTURE_DIRS = [
    os.path.join(PROJECT_ROOT, "fixtures"),
]

if DEBUG:
    TEMPLATES[0]["OPTIONS"]["context_processors"].append("hedera.context_processors.vue_debug")


SESSION_COOKIE_NAME = "sv-sessionid"

ACCOUNT_OPEN_SIGNUP = True
ACCOUNT_EMAIL_UNIQUE = True
ACCOUNT_EMAIL_CONFIRMATION_REQUIRED = False
ACCOUNT_LOGIN_REDIRECT_URL = "home"
ACCOUNT_LOGOUT_REDIRECT_URL = "home"
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 7
ACCOUNT_USE_AUTH_AUTHENTICATE = True

# LTI configuration

CSRF_COOKIE_SAMESITE = None
CSRF_COOKIE_SECURE = True

LTI_TOOL_CONFIGURATION = {
    "title": "Hedera",
    "description": "An LTI-compliant tool that enables users to interact with lemmatized texts.",
    "launch_url": "lti/lti_initializer/",
    "embed_url": "",
    "embed_icon_url": "",
    "embed_tool_id": "",
    "navigation": True,
    "new_tab": False,
    "course_aware": False
}


PYLTI_CONFIG = {
    "consumers": {
        os.environ.get("CONSUMER_KEY"): {
            "secret": os.environ.get("LTI_SECRET")
        }
    }
}

X_FRAME_OPTIONS = os.environ.get("X_FRAME_OPTIONS", "ALLOW-FROM https://canvas.harvard.edu")

# This setting will add an LTI property to the session
LTI_PROPERTY_LIST_EX = ["custom_canvas_course_id", "lis_person_contact_email_primary"]

if IS_LTI:
    AUTHENTICATION_BACKENDS = [
        "hedera.backends.UsernameAuthenticationBackend",
        "lti_provider.auth.LTIBackend",
    ]
else:
    AUTHENTICATION_BACKENDS = [
        "hedera.backends.UsernameAuthenticationBackend",
        # "account.auth_backends.UsernameAuthenticationBackend",
    ]


LOGIN_URL = "account_login"
LTI_REGISTER_URL = "lti_registration"

EMAIL_BACKEND = os.environ.get("EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend")
EMAIL_HOST = os.environ.get("EMAIL_HOST", "")
EMAIL_PORT = os.environ.get("EMAIL_PORT", "")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "")
EMAIL_USE_TLS = True

TEXT_PROVIDER_BACKENDS = [
    "databasetext.backends.TextProviderBackend",
]

# ISO 639.2 CODES
SUPPORTED_LANGUAGES = [
    ["grc", "Ancient Greek"],
    ["lat", "Latin"],
    ["rus", "Russian"],
]


SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
SESSION_COOKIE_SAMESITE = None
