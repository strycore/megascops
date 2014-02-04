# -*- coding: utf8 -*-
from os.path import join, abspath, dirname

## Project
PROJECT_ROOT = abspath(dirname(dirname(__file__)))
DEBUG = True
TEMPLATE_DEBUG = DEBUG
ADMINS = (
    ('Mathieu Comandon', 'strider@strycore.com'),
)
MANAGERS = ADMINS
ROOT_URLCONF = 'megascops.urls'
WSGI_APPLICATION = 'megascops.wsgi.application'
SECRET_KEY = 'q-vep-mg6!hcrcgp=8-5ngu)!bs2limcdt1w(vvt=qup%0anak'

## Databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': join(PROJECT_ROOT, 'megascops.db'),
    }
}

## Apps
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',

    'django_nose',
    'compressor',
    'south',
    'djcelery',
    'sorl.thumbnail',

    'video',
)

## Localization
TIME_ZONE = 'Europe/Paris'
LANGUAGE_CODE = 'en-us'

## Static files
MEDIA_ROOT = join(PROJECT_ROOT, "media")
MEDIA_URL = "/media/"
STATIC_ROOT = join(PROJECT_ROOT, 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = (join(PROJECT_ROOT, 'components'),)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

## Templates
TEMPLATE_DIRS = (join(PROJECT_ROOT, 'templates'),)
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
)

## Middleware
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

## Authentication
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)
LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/"
LOGIN_ERROR_URL = "/accounts/login/error/"

## Email
EMAIL_SUBJECT_PREFIX = "[Megascops]"
DEFAULT_FROM_EMAIL = "strider@strycore.com"

## Celery
CELERY_ROUTES = {
    'video.tasks.fetch_video': {'queue': 'quvi'},
    'video.tasks.encode_videos': {'queue': 'quvi'},
}
import djcelery
djcelery.setup_loader()

## Logging
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

## Testing
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

## Megascops
DEFAULT_SIZE_QUOTA = 52428800
DEFAULT_VIDEO_QUOTA = 5
