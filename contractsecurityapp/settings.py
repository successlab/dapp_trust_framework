import json
import os

from pathlib import Path
import joblib

from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-*5gxx+o_3x@k9a34o2s@tsw7)u$!6rvh52+vmila#+^d31fm2u"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

"""
Environment Types
Local, CI, Test, Prod, DataExtraction, Docker
"""

try:
    ENV_TYPE = os.environ["ENV_TYPE"]
except:
    load_dotenv()
    ENV_TYPE = os.environ["ENV_TYPE"]

# Application definition

INSTALLED_APPS = [
    # Django defaults
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third party apps
    "rest_framework",
    "celery",

    # Custom apps
    "contract_relations.apps.ContractRelationsConfig",
    "web3js_trust.apps.Web3JsTrustConfig",
    "trust_scoring.apps.TrustScoringConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "trust_scoring.middlewares.CorsMiddleware",
]

ROOT_URLCONF = "contractsecurityapp.urls"

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

WSGI_APPLICATION = "contractsecurityapp.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

docker_envs = ["Prod", "Docker", "local_prod"]
if ENV_TYPE in docker_envs:
    print("Connecting to Postgres")
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'postgres',
            'USER': 'postgres',
            'PASSWORD': 'password',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }

else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Github cookie
try:
    from app_secrets.cookies import github_cookie

    header_to_read = github_cookie
    GITHUB_COOKIE = header_to_read

except Exception as e:
    read_cookie = os.environ["GHUB_COOKIE"]
    print("Env Type: " + os.environ["ENV_TYPE"])
    print("Cookie read from the env: " + read_cookie)
    # cookie_to_add = json.loads(os.environ["GHUB_COOKIE"])

# Github header
try:
    from app_secrets.cookies import github_header

    header_to_read = github_header
    GITHUB_HEADER = header_to_read

except Exception as e:
    read_header = os.environ["GITHUB_HEADER"]
    print("Env Type: " + os.environ["ENV_TYPE"])
    print("Header read from the env: " + read_header)
    # cookie_to_add = json.loads(os.environ["GHUB_COOKIE"])

# GITHUB_COOKIE = cookie_to_add
WEB3_HTTP_PROVIDER = os.environ["INFURA_KEY_URL"]
ETHERSCAN_API_KEY = os.environ["ETHERSCAN_API_KEY"]


if ENV_TYPE == "DataExtraction":
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'file': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': os.path.join(BASE_DIR, 'logs/server.log'),
            },
        },
        'loggers': {
            'django': {
                'handlers': ['file'],
                'level': 'DEBUG',
                'propagate': True,
            },
        },
    }

SCORING_ML_MODEL = joblib.load(os.path.join(BASE_DIR, 'random_forest_clf_model.joblib'))

# Celery configuration
CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672//'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'


# ML model settings
TRANSACTIONS_LIMIT_IN_MONTHS = 600