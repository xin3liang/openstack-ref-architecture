Name:		erp-openstack-cli
Version:	2016.12
Release:	4%{?dist}
Summary:	OpenStack CLI venv

License:	Apache
Source0:	openstack-cli.tgz

Requires:	python

%description

%prep
%setup -q -n openstack-cli

%install
install -d %{buildroot}/srv/openstack-cli %{buildroot}/usr/bin
pwd
cp -a * %{buildroot}/srv/openstack-cli/
cd %{buildroot}
for cmd in openstack nova neutron
do
    ln -sf /srv/openstack-cli/bin/$cmd %{buildroot}/usr/bin/$cmd
done

%files
/srv/openstack-cli
/usr/bin

%changelog
* Thu Dec 08 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-4
- move binaries to /usr/bin

* Tue Dec 06 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-3
- Update to newest virtualenv tarballs built for CentOS

* Mon Nov 28 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-2
- own only own directory in /srv

* Thu Nov 10 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-1
- added deps from ansible
