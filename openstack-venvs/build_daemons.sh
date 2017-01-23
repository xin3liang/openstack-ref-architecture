#!/bin/bash -e

if  [ -z $NOSERVICES ]  ; then
       mkdir -p $VENV/systemd-services/
       cp $(dirname $(readlink -f $0))/services/erp-${PROJECT_NAME}* $VENV/systemd-services/
fi
