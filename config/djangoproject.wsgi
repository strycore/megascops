from os import environ
from os.path import dirname, abspath, join
import sys
import site

PROJECT = 'project_name'
PROJECT_ROOT = dirname(dirname(dirname(abspath(__file__))))
site_packages = join(PROJECT_ROOT,
                     'lib/python2.7/site-packages')
site.addsitedir(abspath(site_packages))
sys.path.insert(0, PROJECT_ROOT)
environ['DJANGO_SETTINGS_MODULE'] = '%s.settings' % PROJECT

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
