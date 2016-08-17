#!/bin/bash -ex

cd $(dirname $(readlink -f $0))

# newton on Aug 17
VENV=/srv/openstack-cli

CLIENTS="
	python-keystoneclient:63d039032cd425ef379ffa83af034b23cc80a674
	python-neutronclient:618bc69660f33f358be70cadc9a4033880fec94e
	python-novaclient:6e416bf2502e0934037ad0dc606f68a25668ccf1
	python-glanceclient:5de07c339503c90634e27de342d23276a8833111
	python-cinderclient:0daa4aa0238f3399e166af8833ef1d2816f361fd
	python-openstackclient:fc7a69e410f217a436f7dae97b35314019a48b1b
"

virtualenv $VENV
mkdir $VENV/src
. $VENV/bin/activate
# openstack requires latest versions of pip, pbr, and setuptools to build itself
pip install --upgrade pip
pip install --upgrade pbr
pip install --upgrade setuptools

for x in $CLIENTS ; do
	cd $VENV/src
	repo=$(echo $x | cut -d: -f1)
	version=$(echo $x | cut -d: -f2)
	git clone https://github.com/openstack/$repo
	cd $repo
	git checkout $version
	pip install -r requirements.txt
	python setup.py install
done

cat >$VENV/setup.sh <<EOF
#!/bin/sh
cmds="openstack nova neutron"
cd /usr/local/bin

for x in \$cmds ; do
	[ -e \$x ] && rm \$x
	ln -s /srv/openstack-cli/bin/\$x /usr/local/bin/
done
EOF
chmod +x $VENV/setup.sh
