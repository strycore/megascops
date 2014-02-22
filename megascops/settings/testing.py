from base import *  # noqa
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
DEBUG = False
NOSE_ARGS = (
    "--cover-erase",
    "--with-xunit",
    "--xunit-file=nosetests.xml",
    "--with-xcoverage",
    "--cover-package=video",
    "--xcoverage-file=coverage.xml"
)
