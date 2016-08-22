#!/bin/sh -e

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

ansible -b -K -i $hosts dev-cloud -m shell -a "echo deb http://repo.linaro.org/ubuntu/leg-ceph jessie main > /etc/apt/sources.list.d/leg-ceph.list"
ansible -b -K -i $hosts dev-cloud -m shell -a "apt-get update && apt-get install -y ceph"
