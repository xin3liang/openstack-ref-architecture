Name:		lds-horizon
Version:	2016.12
Release:	2%{?dist}
Summary:	OpenStack horizon venv

License:	Apache
Source0:	horizon.tgz

Requires:	httpd mod_wsgi

%description

%package src
Summary:	OpenStack horizon venv src
%description src

%prep
%setup -q -n horizon
rm     setup.sh
rm -rf src/.git

%install
install -d \
           %{buildroot}/srv/horizon \
           %{buildroot}/etc/apache2/sites-enabled

cp -a * %{buildroot}/srv/horizon/
cd %{buildroot}
ln -sf /srv/horizon/apache.conf %{buildroot}/etc/apache2/sites-enabled/horizon.conf # to check paths

%files src
/srv/horizon/src

%files
/srv/horizon/bin
/srv/horizon/include
/srv/horizon/lib*
/srv/horizon/share
/srv/horizon/apache.conf
/etc/apache2/sites-enabled/horizon.conf

%changelog
* Mon Nov 28 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-2
- changed list of files to not own whole /etc

* Thu Nov 10 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-1
- added deps from ansible
