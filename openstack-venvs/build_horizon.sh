#!/bin/bash -ex

cd $(dirname $(readlink -f $0))

# newton on Aug 22
VERSION="a95159d1482e59920512c3af1915401d13841609"
GIT_URL="https://github.com/openstack/horizon.git"
VENV=/srv/horizon

# we do not have systemd services
NOSERVICES=1

virtualenv $VENV
git clone $GIT_URL $VENV/src
cd $VENV/src
git checkout $VERSION

cd $VENV

cat >$VENV/src/openstack_dashboard/local/local_settings.d/enable_compress.py <<EOF
# minify static files, etc
COMPRESS_OFFLINE = True
COMPRESS_ENABLED = True
EOF

. bin/activate
pip install --upgrade setuptools

pip install pytz
pip install -r src/requirements.txt
pip install python-memcached

# https://bugs.linaro.org/show_bug.cgi?id=2817
pip install python_novaclient==6.0.0

# Adding dependancy due to upstream bug
# https://bugs.launchpad.net/horizon/+bug/1643689
# TODO: remove later
pip install -U "XStatic-roboto-fontface==0.4.3.2"

pip install -U "XStatic_Angular==1.4.10.1"
pip install -U "XStatic_Angular_Bootstrap==0.11.0.8"

./src/manage.py collectstatic --noinput
./src/manage.py compress
./src/manage.py make_web_conf --wsgi
./src/manage.py make_web_conf --apache --hostname horizon > $VENV/apache.conf

cat >$VENV/setup.sh <<EOF
#!/bin/sh
conf=/etc/apache2/sites-enabled/horizon.conf
if [ -f /etc/redhat-release ]; then
   conf=/etc/httpd/conf.d/horizon.conf
fi
[ -f \$conf ] && rm \$conf
ln -s /srv/horizon/apache.conf \$conf
EOF
chmod +x $VENV/setup.sh
