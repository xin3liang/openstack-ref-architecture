#!/bin/bash -ex

HERE=$(dirname $(readlink -f $0))
cd $HERE

# newton on Aug 16
VERSION="7df813bba423f79bc163cd7fc7dd194791f31d21"
GIT_URL="https://github.com/openstack/glance.git"

DESC="Glance API server"
PROJECT_NAME=glance
NAME=glance-api
PROVIDES=glance-api
DAEMON=/srv/glance/bin/glance-api
CONFIG_FILE=/etc/glance/glance-api.conf
source ./build_component.sh

DESC="Glance registry server"
NAME="glance-registry"
PROVIDES=glance-registry
DAEMON=/srv/glance/bin/glance-registry
CONFIG_FILE=/etc/glance/glance-registry.conf
cd $HERE
source ./build_daemons.sh
