#!/bin/bash -ex

HERE=$(dirname $(readlink -f $0))
cd $HERE

# newton on Aug 22
VERSION="bafc5081f436e819fc77e3c852b390676ba19b78"
GIT_URL="https://github.com/openstack/nova.git"

DESC="OpenStack Compute API"
PROJECT_NAME=nova
NAME=nova-api
PROVIDES=nova-api
DAEMON=/srv/nova/bin/nova-api
CONFIG_FILE=/etc/nova/nova.conf
source ./build_component.sh

# APPLY PATCH UEFI shutdown patch
# https://review.openstack.org/#/c/335512/4
git fetch git://git.openstack.org/openstack/nova refs/changes/12/335512/4 && git cherry-pick FETCH_HEAD
python setup.py install
pip install -U libvirt_python==2.2.0

cd $HERE

DESC="Nova Cert server"
NAME=nova-cert
PROVIDES=nova-cert
DAEMON=/srv/nova/bin/nova-cert
source ./build_daemons.sh

DESC="Nova Scheduler"
NAME=nova-scheduler
PROVIDES=$NAME
DAEMON=/srv/nova/bin/$NAME
source ./build_daemons.sh

DESC="OpenStack Compute Console"
NAME=nova-consoleauth
PROVIDES=$NAME
DAEMON=/srv/nova/bin/$NAME
source ./build_daemons.sh

DESC="Nova Conductor server"
NAME=nova-conductor
PROVIDES=$NAME
DAEMON=/srv/nova/bin/$NAME
source ./build_daemons.sh

DESC="Nova Compute server"
NAME=nova-compute
PROVIDES=$NAME
DAEMON=/srv/nova/bin/$NAME
CONFIG_FILE=/etc/nova/nova-compute.conf
DAEMON_ARGS="--config-file=/etc/nova/nova.conf"
source ./build_daemons.sh
