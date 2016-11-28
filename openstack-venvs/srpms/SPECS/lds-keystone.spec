Name:		lds-keystone
Version:	2016.12
Release:	1%{?dist}
Summary:	OpenStack keystone venv

License:	Apache
Source0:	keystone.tgz

Requires:	httpd mod_wsgi MySQL-python

%description

%package src
Summary:	OpenStack keystone venv src
%description src

%prep
%setup -q -n keystone
rm     setup.sh
rm -rf src/.git

%install
install -d \
           %{buildroot}/srv/keystone \
           %{buildroot}/etc/keystone \
           %{buildroot}/etc/apache2/sites-enabled

cp -a * %{buildroot}/srv/keystone/
cp -a src/etc/* %{buildroot}/etc/keystone/

cd %{buildroot}
ln -sf /srv/keystone/apache.conf %{buildroot}/etc/apache2/sites-enabled/keystone.conf # to check paths


%files src
/srv/keystone/src

%files
/srv/keystone/bin
/srv/keystone/etc
/srv/keystone/include
/srv/keystone/lib*
/srv/keystone/apache.conf
/srv/keystone/pip-selfcheck.json
/etc

%changelog
* Tue Nov 15 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-1
- handle /etc/keystone directory
- added deps from ansible
