Name:		erp-keystone
Version:	2016.12
Release:	5%{?dist}
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
           %{buildroot}/etc/keystone

cp -a * %{buildroot}/srv/keystone/
cp -a src/etc/* %{buildroot}/etc/keystone/
rm -f %{buildroot}/srv/keystone/apache.conf

%files src
/srv/keystone/src

%files
/srv/keystone/bin
/srv/keystone/etc
/srv/keystone/include
/srv/keystone/lib*
/srv/keystone/pip-selfcheck.json
/etc/keystone

%changelog
* Fri Dec 09 2016 linaro - 2016.12-5
- rebuild with centos-virtualenv 11 build

* Tue Dec 06 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-4
- Update to newest virtualenv tarballs built for CentOS

* Mon Dec 05 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-3
- removed apache config - #2687

* Mon Nov 28 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-2
- changed list of files to not own whole /etc

* Tue Nov 15 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-1
- handle /etc/keystone directory
- added deps from ansible
