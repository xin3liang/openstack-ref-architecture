#!/bin/sh -e

cd $(dirname $(readlink -f $0))

components="keystone openstack-cli glance neutron nova horizon cinder heat"

for x in $components ; do
	echo === Cleanup old build of $x
	rm -rf /srv/$x
	echo === Building $x
	./build_${x}.sh
done

cd /srv
for x in $components ; do
	echo === Tarballing $x
	tar --exclude ${x}/src/.git -czf /tmp/${x}.tgz $x
done
sha256sum /tmp/*.tgz
