#!/bin/bash -ex

HERE=$(dirname $(readlink -f $0))
cd $HERE

# newton on Aug 19
VERSION="4eee944e9b4588e6b94ca5325eaabd22654fa353"
GIT_URL="https://github.com/openstack/heat.git"

DESC="Heat API"
PROJECT_NAME=heat
NAME=heat-api
PROVIDES=heat-api
DAEMON=/srv/heat/bin/heat-api
CONFIG_FILE=/etc/heat/heat.conf
source ./build_component.sh

cd $HERE

DESC="Heat Cloud Formation"
NAME=heat-api-cfn
PROVIDES=$NAME
DAEMON=/srv/heat/bin/heat-api-cfn
source ./build_daemons.sh

DESC="Heat Engine"
NAME=heat-engine
PROVIDES=$NAME
DAEMON=/srv/heat/bin/heat-engine
source ./build_daemons.sh
