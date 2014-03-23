"""
WSGI config for megascops project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
# pylint: disable=C0103
import os
import sys
import site
from os.path import dirname, abspath, join

PROJECT = 'megascops'
PROJECT_ROOT = dirname(dirname(dirname(abspath(__file__))))
SITE_PACKAGES = join(PROJECT_ROOT, 'lib/python2.7/site-packages')
site.addsitedir(abspath(SITE_PACKAGES))
sys.path.insert(0, PROJECT_ROOT)
sys.path.append(join(PROJECT_ROOT, PROJECT))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "megascops.settings.local")

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
