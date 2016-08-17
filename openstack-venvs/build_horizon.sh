#!/bin/bash -ex

cd $(dirname $(readlink -f $0))

# newton on Aug 16
VERSION="450baeed4fe74736d0f0825256f758fc4ab099c6"
GIT_URL="https://github.com/openstack/horizon.git"
VENV=/srv/horizon

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
pip install -r src/requirements.txt
pip install python-memcached

./src/manage.py collectstatic --noinput
./src/manage.py compress
./src/manage.py make_web_conf --wsgi
./src/manage.py make_web_conf --apache --hostname horizon > $VENV/apache.conf

cat >$VENV/setup.sh <<EOF
#!/bin/sh
conf=/etc/apache2/sites-enabled/horizon.conf
[ -f \$CONF ] && rm \$CONF
ln -s /srv/horizon/apache.conf \$conf
EOF
chmod +x $VENV/setup.sh
