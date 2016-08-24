#!/bin/bash -ex

HERE=$(dirname $(readlink -f $0))
cd $HERE

# newton on Aug 22
VERSION="8c2ed599dcfa2d3d1bab7b97ecc423df0cf33bc6"
GIT_URL="https://github.com/openstack/cinder.git"

DESC="OpenStack Block Storage Scheduler"
PROJECT_NAME=cinder
NAME=cinder-scheduler
PROVIDES=$NAME
DAEMON=/srv/cinder/bin/cinder-scheduler
CONFIG_FILE=/etc/cinder/cinder.conf
source ./build_component.sh

cd $HERE

DESC="OpenStack Block Storage API"
PROJECT_NAME=cinder
NAME=cinder-api
PROVIDES=$NAME
DAEMON=/srv/cinder/bin/cinder-api
CONFIG_FILE=/etc/cinder/cinder.conf
source ./build_daemons.sh

DESC="OpenStack Block Storage Volume"
PROJECT_NAME=cinder
NAME=cinder-volume
PROVIDES=$NAME
DAEMON=/srv/cinder/bin/cinder-volume
CONFIG_FILE=/etc/cinder/cinder.conf
source ./build_daemons.sh
