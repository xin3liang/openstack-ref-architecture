#!/bin/sh -e

if [ $# -eq 0 ] ; then
	echo "Usage: $0 <admin_node>"
	exit 1
fi

set -x

hosts=$(mktemp)
trap "rm -rf $hosts" EXIT
echo "[dev-cloud]" > $hosts
echo $1 >> $hosts

ansible -b -i $hosts $1 -m shell -a "ceph osd pool create images 64"
ansible -b -i $hosts $1 -m shell -a "ceph auth get-or-create client.images mon 'allow r' osd 'allow class-read object_prefix rbd_children, allow rwx pool=images' -o /etc/ceph/ceph.client.images.keyring"

ansible -b -i $hosts $1 -m shell -a "ceph osd pool create vms 128"
ansible -b -i $hosts $1 -m shell -a "ceph auth get-or-create client.nova mon 'allow r' osd 'allow class-read object_prefix rbd_children, allow rwx pool=vms, allow rwx pool=images' -o /etc/ceph/ceph.client.nova.keyring"

ansible -b -i $hosts $1 -m shell -a "ceph osd pool create volumes 64"
ansible -b -i $hosts $1 -m shell -a "ceph auth get-or-create client.cinder mon 'allow r' osd 'allow class-read object_prefix rbd_children, allow rwx pool=volumes, allow rwx pool=vms, allow rx pool=images' -o /etc/ceph/ceph.client.cinder.keyring"
