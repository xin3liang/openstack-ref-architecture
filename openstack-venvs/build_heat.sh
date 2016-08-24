#!/bin/bash -ex

HERE=$(dirname $(readlink -f $0))
cd $HERE

# newton on Aug 22
VERSION="50ee32f846cbdf64887ad629eeb3fb6e03ab7acf"
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
