#!/bin/sh -e

# we don't have ceph packaged in a way that ceph-deploy can use,
# so here's a quick hack to install

if [ $# -eq 0 ] ; then
	echo "Usage: $0 <node1> [node2 ...]"
	exit 1
fi

set -x

hosts=$(mktemp)
trap "rm -rf $hosts" EXIT
echo "[dev-cloud]" > $hosts
for x in $* ; do
	echo $x >> $hosts
done

ansible -b -K -i $hosts dev-cloud -m shell -a "wget -O /tmp/ceph.tgz http://people.linaro.org/~andy.doan/devcloud/ceph.tgz"
ansible -b -K -i $hosts dev-cloud -m shell -a "cd /tmp && tar -xzf ceph.tgz && sudo /tmp/ceph/setup.sh"
