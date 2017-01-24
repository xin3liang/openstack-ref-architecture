#!/bin/bash -ex

HERE=$(dirname $(readlink -f $0))
cd $HERE

# newton on Aug 22
VENV=/srv/openstack-cli

CLIENTS="
	python-keystoneclient:1b5c8bad80319dd78104c148fd34b59a825a7a36
	python-neutronclient:3c5b2839bf37ff92212158acb6f20957e0eb7c96
	python-novaclient:3b834f25c1d31ef482116344f97b0a1059d9a836:
	python-glanceclient:d4196325eb05dadfaf62d8facbd8c6fe50f72166
	python-cinderclient:f802d1ae1add84a3cd590de596d7835c1fce79b3
	python-openstackclient:684412ca4cc0abad2c2a800d8247d12992b994e5
"

virtualenv $VENV
mkdir $VENV/src
. $VENV/bin/activate

# openstack requires latest versions of pip, pbr, and setuptools to build itself
pip install --upgrade pip==9.0.1
pip install --upgrade pbr==1.10.0
pip install --upgrade setuptools==33.1.1

pip install pytz==2016.10

# generated from Debian build #21
pip install -r $HERE/pips/openstack-cli.pipreqs -r $HERE/pips/common.pipreqs

for x in $CLIENTS ; do
	cd $VENV/src
	repo=$(echo $x | cut -d: -f1)
	version=$(echo $x | cut -d: -f2)
	git clone https://github.com/openstack/$repo
	cd $repo
	git checkout -b $version $version
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
