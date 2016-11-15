#!/bin/sh

. /srv/horizon/bin/activate
python /srv/horizon/src/manage.py collectstatic --noinput
python /srv/horizon/src/manage.py compress
