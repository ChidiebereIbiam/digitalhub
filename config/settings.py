"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import django
import environ
import os


from django.utils.encoding import force_str
django.utils.encoding.force_text = force_str

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
APPS_DIR = BASE_DIR / "digitalhub"

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


# False if not in os.environ because of casting above
DEBUG = env('DEBUG')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
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

    #Local Apps
    'digitalhub.blog',
    'digitalhub.core',
    'digitalhub.authentication',
    'digitalhub.userbase',
    'digitalhub.payment',

    #Third Party Apps
    "crispy_forms",
    "crispy_bootstrap5",
    'ckeditor',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.apple',
    'allauth.socialaccount.providers.google',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "allauth.account.middleware.AccountMiddleware",
]

SITE_ID = 1

ROOT_URLCONF = 'config.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.app'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_USER_MODEL = 'authentication.User'
# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

# STATIC_ROOT = str(BASE_DIR / "staticfiles")
STATIC_URL = 'static/'

STATICFILES_DIRS = [str(APPS_DIR / "static")]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]
# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK = "bootstrap5"
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"


# django-allauth
# ------------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

ACCOUNT_ALLOW_REGISTRATION = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_EMAIL_NOTIFICATIONS = True
ACCOUNT_EMAIL_SUBJECT_PREFIX = "localhost"
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_FORMS = {"signup": "digitalhub.authentication.forms.UserSignupForm"}
EMAIL_CONFIRM_REDIRECT_BASE_URL = "http://localhost:8000/email/confirm/"
PASSWORD_RESET_CONFIRM_REDIRECT_BASE_URL = "http://localhost:8000/password-reset/confirm/"
ACCOUNT_LOGOUT_REDIRECT_URL = 'account_login'
# SOCIALACCOUNT_ADAPTER = "digitalhub.authentication.adapters.SocialAccountAdapter"
# SOCIALACCOUNT_FORMS = {"signup": "digitalhub.authentication.forms.UserSocialSignupForm"}

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'EMAIL_AUTHENTICATION': True,
        'APP': {
            'client_id': env('GOOGLE_CLIENT_ID'),
            'secret': env('GOOGLE_CLIENT_SECRET'),
            'key': env('GOOGLE_CLIENT_KEY')
        },
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
        'OAUTH_PKCE_ENABLED': True,
    },
    "apple": {
        "APPS": [{
            "client_id": env('APPLE_CLIENT_ID'),
            "secret": env('APPLE_CLIENT_SECRET'),
            "key": env('APPLE_CLIENT_KEY'),

            "settings": {
                "certificate_key": env('APPLE_CERTIFICATE_KEY'),
            }
        }]
    }
}



# Email Settings
# ------------------------------------------------------------------------------
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = "no_reply@localhost.com"
DEFAULT_EMAIL = "info@locahost.com"


LOGIN_URL = "account_login"
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = 'account_login'

# Strip Settings
# ------------------------------------------------------------------------------
STRIPE_PUBLISHABLE_KEY = env('STRIPE_PUBLISHABLE_KEY')
STRIPE_SECRET_KEY = env('STRIPE_SECRET_KEY')
STRIPE_ENDPOINT_SECRET = env('STRIPE_ENDPOINT_SECRET')
DOMAIN_URL = env('DOMAIN_URL')