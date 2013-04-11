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
SITE_ID = 1
SITE_NAME = "http://megascops.org/"
ROOT_URLCONF = 'megascops.urls'
WSGI_APPLICATION = 'megascops.wsgi.application'
SECRET_KEY = 'q-vep-mg6!hcrcgp=8-5ngu)!bs2limcdt1w(vvt=qup%0anak'
ALLOWED_HOSTS = ("megascops.strycore.com", "megascops.org")

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

    'registration',
    'compressor',
    'south',
    'djcelery',
    'social_auth',
    'sorl.thumbnail',

    'video',
)

## Localization
TIME_ZONE = 'Europe/Paris'
LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = True
USE_TZ = True
## Static files
MEDIA_ROOT = join(PROJECT_ROOT, "media")
MEDIA_URL = "/media/"
STATIC_ROOT = join(PROJECT_ROOT, 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = (join(PROJECT_ROOT, 'components'),)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
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
    #'social_auth.context_processors.social_auth_by_name_backends',
    'social_auth.context_processors.social_auth_backends',
    #'social_auth.context_processors.social_auth_by_type_backends',
    'social_auth.context_processors.social_auth_login_redirect',
)

## Middleware
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

## Compressor
COMPRESS_ENABLED = False
COMPRESS_PRECOMPILERS = (
    ('text/coffeescript', 'coffee --compile --stdio'),
    ('text/less', 'lessc {infile} {outfile}'),
)

## Authentication
AUTHENTICATION_BACKENDS = (
    'social_auth.backends.twitter.TwitterBackend',
    #'social_auth.backends.facebook.FacebookBackend',
    #'social_auth.backends.google.GoogleOAuthBackend',
    #'social_auth.backends.google.GoogleOAuth2Backend',
    #'social_auth.backends.google.GoogleBackend',
    #'social_auth.backends.yahoo.YahooBackend',
    #'social_auth.backends.browserid.BrowserIDBackend',
    #'social_auth.backends.contrib.linkedin.LinkedinBackend',
    #'social_auth.backends.contrib.livejournal.LiveJournalBackend',
    #'social_auth.backends.contrib.orkut.OrkutBackend',
    #'social_auth.backends.contrib.foursquare.FoursquareBackend',
    #'social_auth.backends.contrib.github.GithubBackend',
    #'social_auth.backends.contrib.vkontakte.VKontakteBackend',
    #'social_auth.backends.contrib.live.LiveBackend',
    #'social_auth.backends.contrib.skyrock.SkyrockBackend',
    #'social_auth.backends.contrib.yahoo.YahooOAuthBackend',
    #'social_auth.backends.OpenIDBackend',
    'django.contrib.auth.backends.ModelBackend',
)
TWITTER_CONSUMER_KEY = 'please put this in Local_settings.py'
TWITTER_CONSUMER_SECRET = 'please put this in local_settings.py'
LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/"
LOGIN_ERROR_URL = "/accounts/login/error/"
#SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/another-login-url/'
#SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/new-users-redirect-url/'
#SOCIAL_AUTH_NEW_ASSOCIATION_REDIRECT_URL = '/new-association-redirect-url/'
#SOCIAL_AUTH_DISCONNECT_REDIRECT_URL = '/account-disconnected-redirect-url/'
#SOCIAL_AUTH_BACKEND_ERROR_URL = '/new-error-url/'
SOCIAL_AUTH_COMPLETE_URL_NAME = 'socialauth_complete'
SOCIAL_AUTH_ASSOCIATE_URL_NAME = 'socialauth_associate_complete'
SOCIAL_AUTH_DEFAULT_USERNAME = 'new_social_auth_user'
SOCIAL_AUTH_EXPIRATION = 'expires'
SOCIAL_AUTH_ASSOCIATE_BY_MAIL = True
ACCOUNT_ACTIVATION_DAYS = 2

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

## Megascops
DEFAULT_SIZE_QUOTA = 52428800
DEFAULT_VIDEO_QUOTA = 5

## Local settings
try:
    from local_settings import *
except ImportError:
    pass
