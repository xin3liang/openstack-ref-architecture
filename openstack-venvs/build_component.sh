#!/bin/bash -ex

VENV=/srv/$PROJECT_NAME

if [ -f /etc/debian_version ]; then
    apt-get -q=2 update
    apt-get install -y git libyaml-dev libxml2-dev libxslt1-dev libmysqlclient-dev libffi-dev libssl-dev libvirt-dev \
                       python-dev pkg-config libvirt-dev python-virtualenv libsasl2-dev libldap2-dev
fi

if [ -f /etc/redhat-release ]; then
    CMD=yum

    if [ -f /etc/fedora-release ]; then
       CMD=dnf
    fi

    $CMD install -y gcc make libyaml-devel libxml2-devel libxslt-devel mysql-devel libffi-devel openssl-devel \
                    libvirt-devel python-devel pkgconfig python-virtualenv git cyrus-sasl-devel openldap-devel
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
pip install --upgrade pip==9.0.1
pip install --upgrade pbr==1.10.0
pip install --upgrade setuptools==33.1.1

pip install pytz==2016.10

# generated from Debian build #21
pip install -r $HERE/pips/${PROJECT_NAME}.pipreqs -r $HERE/pips/components-common.pipreqs -r $HERE/pips/common.pipreqs

cd $VENV/src
pip install -r requirements.txt
python setup.py install
