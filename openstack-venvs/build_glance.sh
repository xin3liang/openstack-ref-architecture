#!/bin/bash -ex

HERE=$(dirname $(readlink -f $0))
cd $HERE

# newton on Aug 22
VERSION="30f7a3c308d05390d0ed3e391aaeb538dbb1a5d8"
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
