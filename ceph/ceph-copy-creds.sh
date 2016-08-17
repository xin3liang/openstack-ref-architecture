#!/bin/sh -e

# copy creditials to all the openstack nodes that need it

if [ $# -lt 2 ] ; then
	echo "Usage: $0 <admin_node> [node1 ...]"
	exit 1
fi

admin=$1
shift
nodes=$*
set -x

hosts=$(mktemp)
trap "rm -rf $hosts /etc/sudoers.d/zz-ceph-deploy" EXIT
echo "[dev-cloud]" > $hosts
echo $admin >> $hosts
for x in $nodes ; do
	echo $x >> $hosts
done

# copy credentials and distribute
for x in ceph.client.images.keyring ceph.client.nova.keyring ceph.client.cinder.keyring ; do
	ansible -b -i $hosts $admin -m fetch -a "src=/etc/ceph/$x dest=./$x flat=yes"
	ansible -b -i $hosts dev-cloud -m copy -a "src=./$x dest=/etc/ceph/$x"
	rm $x
done
