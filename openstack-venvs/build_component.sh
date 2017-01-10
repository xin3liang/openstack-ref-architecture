#!/bin/bash -ex

VENV=/srv/$PROJECT_NAME

if [ -f /etc/debian_version ]; then
    apt-get -q=2 update
    apt-get install -y git libyaml-dev libxml2-dev libxslt1-dev libmysqlclient-dev libffi-dev libssl-dev libvirt-dev python-dev pkg-config libvirt-dev python-virtualenv
fi

if [ -f /etc/redhat-release ]; then
    CMD=yum

    if [ -f /etc/fedora-release ]; then
	CMD=dnf
    fi

    $CMD install -y gcc make libyaml-devel libxml2-devel libxslt-devel mysql-devel libffi-devel openssl-devel libvirt-devel python-devel pkgconfig python-virtualenv git
fi

rm -rf $VENV

virtualenv $VENV

source ./build_daemons.sh

# copy setup script
cat ./setup.sh.tmpl | sed -e "s/#PROJECT_NAME#/${PROJECT_NAME}/g" > $VENV/setup.sh
chmod +x $VENV/setup.sh

git clone $GIT_URL $VENV/src
cd $VENV/src
git config user.email "ci_notifications@linaro.org"
git config user.name "Jenkins"
git checkout -b $VERSION $VERSION

. $VENV/bin/activate
# openstack requires latest versions of pip, pbr, and setuptools to build itself
pip install --upgrade pip
pip install --upgrade pbr
pip install --upgrade setuptools

# Newton requires 3.0 version of kombu and its now 4.0
pip install kombu==3.0.35
pip install vine==1.1.3

pip install eventlet==0.19.0
pip install tenacity==3.4.0

# let use the same as we had in CentOS #14
# jinja2 2.9.4 causes rpm packages build failure
pip install jinja2==2.8.1

# https://bugs.linaro.org/show_bug.cgi?id=2802
pip install webob==1.6.3

# add requirements based on our deployment choices
cp $VENV/src/requirements.txt $VENV/src/reqs.txt
echo "python-memcached" >> $VENV/src/reqs.txt
echo "pymysql" >> $VENV/src/reqs.txt

if [ "$PROJECT_NAME" == "nova" ] ; then
	sed -i '1s/^/pytz\n/' $VENV/src/reqs.txt
	cat >> $VENV/src/reqs.txt <<EOF
monotonic
debtcollector
python-dateutil
fasteners
positional
functools32
tempita
sqlparse
kombu
cachetools
cliff
libvirt-python
retrying
futurist
EOF
fi

cd $VENV/src
pip install -r reqs.txt
python setup.py install
