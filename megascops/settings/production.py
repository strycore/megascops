import os
from base import *  # noqa

DEBUG = False
SECRET_KEY = os.environ['SECRET_KEY']
ALLOWED_HOSTS = ("megascops.strycore.com", "megascops.org")

STATICFILES_STORAGE = (
    'django.contrib.staticfiles.storage.CachedStaticFilesStorage'
)
