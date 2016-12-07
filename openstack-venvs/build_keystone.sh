#!/bin/bash -ex

cd $(dirname $(readlink -f $0))

# newton on Aug 22
VERSION="0cd732b2b0d3e18cbdbceecf66a83cd378c27717"
GIT_URL="https://github.com/openstack/keystone.git"

DESC="OpenStack cloud identity service"
PROJECT_NAME=keystone
PROVIDES=keystone
NAME=keystone-all
DAEMON=/srv/keystone/bin/keystone-all
CONFIG_FILE=/etc/keystone/keystone.conf

# we do not have systemd services
NOSERVICES=1

source ./build_component.sh
/srv/keystone/bin/pip install python-openstackclient
