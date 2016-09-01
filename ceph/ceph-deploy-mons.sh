#!/bin/sh -e

if ! which ceph-deploy ; then
	echo "ERROR: ceph-deploy must be installed (via pip or apt)"
	exit 1
fi
if [ -z $SSH_USER ] ; then
	echo "ERROR: SSH_USER environment variable required"
	exit 1
fi
if [ $# -eq 0 ] ; then
	echo "Usage: $0 <node1> [node2 ...]"
	exit 1
fi

set -x

hosts=$(mktemp)
trap "rm -rf $hosts /etc/sudoers.d/zz-ceph-deploy" EXIT
echo "[dev-cloud]" > $hosts
for x in $* ; do
	echo $x >> $hosts
done

# ceph-deploy requires a passwordless sudoer, this creates a hack to enable
ansible -b -K -i $hosts dev-cloud -m shell -a "echo $SSH_USER ALL=\(ALL\) NOPASSWD:ALL > /etc/sudoers.d/zz-ceph-deploy"

ceph-deploy new $*
cat >> ceph.conf <<EOF

# needed for raw directories rather than disks
#osd max object name len = 256
#osd max object namespace len = 64

[client.images]
keyring = /etc/ceph/ceph.client.images.keyring

[client.nova]
keyring = /etc/ceph/ceph.client.nova.keyring

[client.cinder]
keyring = /etc/ceph/ceph.client.cinder.keyring
EOF

ceph-deploy mon create-initial
ceph-deploy admin $*
