#!/bin/bash -ex

HERE=$(dirname $(readlink -f $0))
cd $HERE

# newton on Aug 22
VERSION="14ebfb527dfa8631db0112f605927449584050ad"
GIT_URL="https://github.com/openstack/neutron.git"

DESC="OpenStack Network API"
PROJECT_NAME=neutron
NAME=neutron-server
PROVIDES=$NAME
DAEMON=/srv/neutron/bin/neutron-server
CONFIG_FILE=/etc/neutron/neutron.conf
source ./build_component.sh

cd $HERE

DESC="Neutron OpenVSwitch Agent"
NAME=neutron-openvswitch-agent
PROVIDES=$NAME
DAEMON=/srv/neutron/bin/neutron-openvswitch-agent
CONFIG_FILE=/etc/neutron/plugins/ml2/openvswitch_agent.ini
DAEMON_ARGS="--config-file=/etc/neutron/neutron.conf --config-file=/etc/neutron/plugins/ml2/openvswitch_agent.ini"
source ./build_daemons.sh

DESC="Neutron Metadata Agent"
NAME=neutron-metadata-agent
PROVIDES=$NAME
DAEMON=/srv/neutron/bin/neutron-metadata-agent
CONFIG_FILE=/etc/neutron/metadata_agent.ini
DAEMON_ARGS="--config-file=/etc/neutron/neutron.conf"
source ./build_daemons.sh

DESC="Neutron DHCP Agent"
NAME=neutron-dhcp-agent
PROVIDES=$NAME
DAEMON=/srv/neutron/bin/neutron-dhcp-agent
CONFIG_FILE=/etc/neutron/dhcp_agent.ini
source ./build_daemons.sh

DESC="Neutron L3 Agent"
NAME=neutron-l3-agent
PROVIDES=$NAME
DAEMON=/srv/neutron/bin/neutron-l3-agent
CONFIG_FILE=/etc/neutron/l3_agent.ini
source ./build_daemons.sh
