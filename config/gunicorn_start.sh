#!/bin/bash

NAME="megascops"
ROOT=/srv/megascops.org
DJANGODIR=$ROOT/project_name
SOCKFILE=$ROOT/run/gunicorn.sock
USER=strider
GROUP=strider
NUM_WORKERS=9
DJANGO_SETTINGS_MODULE=megascops.settings.production
DJANGO_WSGI_MODULE=megascops.wsgi

echo "Starting $NAME as `whoami`"

cd $DJANGODIR
source ../bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH
source ../bin/envvars

RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

exec ../bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
    --name $NAME \
    --workers $NUM_WORKERS \
    --user=$USER --group=$GROUP \
    --log-level=debug \
    --bind=unix:$SOCKFILE
