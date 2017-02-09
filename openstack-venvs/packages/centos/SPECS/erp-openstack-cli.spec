Name:		erp-openstack-cli
Version:	2016.12.build31
Release:	9%{?dist}
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
/usr/bin/openstack
/usr/bin/nova
/usr/bin/neutron

%changelog
* Thu Feb 09 2017 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12.build31-9
- rebuild with virtualenv build 31

* Tue Jan 31 2017 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12.build30-8
- rebuild with virtualenv build 30

* Wed Jan 25 2017 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12.build27-7
- rebuild with virtualenv build 27

* Tue Jan 24 2017 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12.build26-6
- Rebuild with CentOS virtualenv tarballs from build #26

* Mon Jan 23 2017 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12.build24-5
- Rebuild with CentOS virtualenv tarballs from build #24
- Fix maintainer name in changelog entries.

* Tue Jan 17 2017 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12.build23-4
- Rebuild with CentOS virtualenv tarballs from build #23

* Fri Jan 13 2017 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12.build21-3
- Rebuild with CentOS virtualenv tarballs from build #21

* Fri Jan 13 2017 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12.build20-2
- Rebuild with CentOS virtualenv tarballs from build #20

* Wed Jan 11 2017 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12.build19-1
- Rebuild with CentOS venv build #19

* Tue Jan 10 2017 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-build17.10
- Rebuild with CentOS virtualenv tarballs from build #17

* Wed Jan 04 2017 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-build14.9
- Use virtualenv tarballs 14
- Use venvs build number in release tag.

* Thu Dec 15 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-8
- rebuild with CentOS virtualenv build 13

* Fri Dec 09 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-7
- fixed /usr/bin ownership - #2742

* Fri Dec 09 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-6
- fixing email in changelog

* Fri Dec 09 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-5
- rebuild with centos-virtualenv 11 build

* Thu Dec 08 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-4
- move binaries to /usr/bin

* Tue Dec 06 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-3
- Update to newest virtualenv tarballs built for CentOS

* Mon Nov 28 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-2
- own only own directory in /srv

* Thu Nov 10 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-1
- added deps from ansible
