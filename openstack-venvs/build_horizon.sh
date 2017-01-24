#!/bin/bash -ex

HERE=$(dirname $(readlink -f $0))
cd $HERE

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

# openstack requires latest versions of pip, pbr, and setuptools to build itself
pip install --upgrade pip==9.0.1
pip install --upgrade setuptools==33.1.1
pip install --upgrade pbr==1.10.0

pip install pytz==2016.10

# generated from Debian build #21
pip install -r $HERE/pips/horizon.pipreqs -r $HERE/pips/common.pipreqs

pip install -r src/requirements.txt

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
