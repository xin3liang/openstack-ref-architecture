#!/bin/bash -ex

cd $(dirname $(readlink -f $0))

# newton on Aug 22
VERSION="0cd732b2b0d3e18cbdbceecf66a83cd378c27717"
GIT_URL="https://github.com/openstack/keystone.git"

DESC="OpenStack cloud identity service"
PROJECT_NAME=keystone
PROVIDES=keystone
NAME=keystone-all
DAEMON=/srv/keystone/bin/keystone-all
CONFIG_FILE=/etc/keystone/keystone.conf

source ./build_component.sh
/srv/keystone/bin/pip install python-openstackclient

cat >/srv/keystone/apache.conf <<EOF
Listen 5000
Listen 35357

<VirtualHost *:5000>
	WSGIDaemonProcess keystone-public processes=5 threads=1 user=keystone group=keystone display-name=%{GROUP} python-path=/srv/keystone/lib/python2.7:/srv/keystone/lib/python2.7/lib-dynload:/srv/keystone/local/lib/python2.7/site-packages:/srv/keystone/lib/python2.7/site-packages
	WSGIProcessGroup keystone-public
	WSGIScriptAlias / /srv/keystone/bin/keystone-wsgi-public
	WSGIApplicationGroup %{GLOBAL}
	WSGIPassAuthorization On
	ErrorLogFormat "%{cu}t %M"
	ErrorLog /var/log/apache2/keystone.log
	CustomLog /var/log/apache2/keystone_access.log combined

	<Directory /srv/keystone/bin>
		Require all granted
	</Directory>
</VirtualHost>

<VirtualHost *:35357>
	WSGIDaemonProcess keystone-admin processes=5 threads=1 user=keystone group=keystone display-name=%{GROUP} python-path=/srv/keystone/lib/python2.7:/srv/keystone/lib/python2.7/lib-dynload:/srv/keystone/local/lib/python2.7/site-packages:/srv/keystone/lib/python2.7/site-packages

	WSGIProcessGroup keystone-admin
	WSGIScriptAlias / /srv/keystone/bin/keystone-wsgi-admin
	WSGIApplicationGroup %{GLOBAL}
	WSGIPassAuthorization On
	ErrorLogFormat "%{cu}t %M"
	ErrorLog /var/log/apache2/keystone.log
	CustomLog /var/log/apache2/keystone_access.log combined

	<Directory /srv/keystone/bin>
		Require all granted
	</Directory>
</VirtualHost>
EOF

# keystone runs from apache so there's no /etc/init.d or systemd servicd
rm /srv/keystone/keystone-init.d
