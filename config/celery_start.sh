#!/bin/bash

DJANGODIR=/src/megascops/megascops
DJANGO_SETTINGS_MODULE=megascops.settings.production

cd $DJANGODIR
source ../bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH
source ../bin/envvars

exec ../bin/celery worker -A megascops.celery.app --loglevel=INFO
