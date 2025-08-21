import os
from pathlib import Path
from config import load_config

RUNNING_IN_DOCKER = os.getenv("RUNNING_IN_DOCKER", "0") == "1"

config = load_config()


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config.project.key

DEBUG = True

ALLOWED_HOSTS = []


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'debug_toolbar',

    "widget_tweaks",

    'clothes.apps.ClothesConfig',
    "users.apps.UsersConfig",
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'debug_toolbar.middleware.DebugToolbarMiddleware',

    'clothes.middleware.set_local_data.set_local_data',
]

ROOT_URLCONF = 'yanki.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                # "clothes.context_processors.settings",
                # "clothes.context_processors.appointment_form",
                # "clothes.context_processors.courses_categories",
            ],
            'builtins': [
                'clothes.templatetags.clothes_tags',

            ],
        },
    },
]

WSGI_APPLICATION = 'yanki.wsgi.application'


INTERNAL_IPS = [
    '127.0.0.1',
]

SITE_NAME = "Yanki"
SITE_ID = 1


LOGOUT_REDIRECT_URL = "http://127.0.0.1:8000"
LOGIN_REDIRECT_URL = "http://127.0.0.1:8000"

AUTH_USER_MODEL = 'users.User'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': config.mail.token,
            'secret': config.mail.key,
            'key': ''
        },
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'}
    }
}


# Database
db_engine = 'django.db.backends.sqlite3'
db_name = BASE_DIR / 'db.sqlite3'
db_user = ''
db_password = ''
db_host = ''
db_port = ''

if RUNNING_IN_DOCKER:
    db_engine = config.db.type
    db_name = config.db.name
    db_user = config.db.user
    db_password = config.db.password
    db_host = config.db.host
    db_port = config.db.port

DATABASES = {
    'default': {
        'ENGINE': db_engine,
        'NAME': db_name,
        'USER': db_user,
        'PASSWORD': db_password,
        'HOST': db_host,
        'PORT': db_port,
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


CART_SESSION_ID = "cart"
CURRENCY_SESSION_ID = "currency"
LIKE_SESSION_ID = "like"
SESSION_SAVE_EVERY_REQUEST = True


# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config.mail.host
EMAIL_PORT = config.mail.port
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config.mail.user
EMAIL_HOST_PASSWORD = config.mail.password
EMAIL_SERVER = config.mail.user
DEFAULT_FROM_EMAIL = config.mail.user
EMAIL_ADMIN = [config.mail.other_user]

# Language and tine settings
LANGUAGE_CODE = 'ru'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Other settings
SITE_URL = "http://127.0.0.1:8000"
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = []

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"
