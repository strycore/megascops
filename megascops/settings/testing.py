from base import *  # noqa
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
INSTALLED_APPS += [
    'django_jenkins'
]
DEBUG = False
