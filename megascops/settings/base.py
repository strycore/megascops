# -*- coding: utf8 -*-
from __future__ import absolute_import
from os.path import join, abspath, dirname

# Project
PROJECT_ROOT = abspath(dirname(dirname(dirname(__file__))))
DEBUG = True
ALLOWED_HOSTS = ('*', )
ADMINS = (
    ('Mathieu Comandon', 'strider@strycore.com'),
)
MANAGERS = ADMINS
SITE_ID = 1
ROOT_URLCONF = 'megascops.urls'
WSGI_APPLICATION = 'megascops.wsgi.application'
SECRET_KEY = 'q-vep-mg6!hcrcgp=8-5ngu)!bs2limcdt1w(vvt=qup%0anak'

# Databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'megascops',
        'USER': 'megascops',
        'PASSWORD': 'admin',
        'HOST': 'localhost'
    }
}

# Apps
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',

    'sorl.thumbnail',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]

PROJECT_APPS = [
    'video'
]

INSTALLED_APPS += PROJECT_APPS

# Localization
TIME_ZONE = 'Europe/Paris'
LANGUAGE_CODE = 'en-us'

# Static files
MEDIA_ROOT = join(PROJECT_ROOT, "media")
MEDIA_URL = "/media/"
STATIC_ROOT = join(PROJECT_ROOT, 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    join(PROJECT_ROOT, "public"),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': (join(PROJECT_ROOT, 'templates'),),
        'OPTIONS': {
            'context_processors': [
                'django.core.context_processors.debug',
                'django.core.context_processors.i18n',
                'django.core.context_processors.media',
                'django.core.context_processors.static',
                'django.core.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            'debug': True
        },
    }
]


# Middleware
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

# Authentication
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_SIGNUP_PASSWORD_VERIFICATION = False
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['https://www.googleapis.com/auth/userinfo.profile'],
        'AUTH_PARAMS': {'access_type': 'online'}
    }
}
LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/"
LOGIN_ERROR_URL = "/accounts/login/error/"

# Email
EMAIL_SUBJECT_PREFIX = "[Megascops]"
DEFAULT_FROM_EMAIL = "strider@strycore.com"


# Celery
BROKER_URL = 'amqp://guest:guest@localhost:5672//'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'include_html': True,
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': join(PROJECT_ROOT, 'megascops.log')
        },
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'file'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.contrib.messages': {
            'handlers': ['mail_admins', 'file'],
            'level': 'ERROR',
            'propagate': True,
        },
        'video': {
            'handlers': ['mail_admins', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

# Megascops
DEFAULT_SIZE_QUOTA = 52428800
DEFAULT_VIDEO_QUOTA = 5
