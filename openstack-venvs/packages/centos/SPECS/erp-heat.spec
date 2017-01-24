Name:		erp-heat
Version:	2016.12.build26
Release:	6%{?dist}
Summary:	OpenStack heat venv

License:	Apache
Source0:	heat.tgz
Source1:	heat.logrotate
Source2:	heat.sudoers

Requires(pre):	shadow-utils

%description

%package services
Summary:	OpenStack heat venv services
Requires(post):   systemd
Requires:	erp-heat
%description services

%package src
Summary:	OpenStack heat venv src
%description src

%prep
%setup -q -n heat
rm     setup.sh
rm -rf src/.git

%install
install -d \
           %{buildroot}/srv/heat \
           %{buildroot}/etc/heat \
           %{buildroot}/usr/lib/systemd/system \
           %{buildroot}/var/log/heat \
           %{buildroot}/var/lib/heat/instances \
           %{buildroot}/etc/heat \
           %{buildroot}/etc/logrotate.d \
           %{buildroot}/etc/sudoers.d

install -m 0644 %{_sourcedir}/heat.logrotate %{buildroot}/etc/logrotate.d/heat
install -m 0644 %{_sourcedir}/heat.sudoers   %{buildroot}/etc/sudoers.d/heat

cp -a * %{buildroot}/srv/heat/
cp -a src/etc/heat/* %{buildroot}/etc/heat/
cp -a systemd-services/* %{buildroot}/usr/lib/systemd/system/

%files src
/srv/heat/src

%files services
/usr/lib/systemd/system/erp-heat-api-cfn.service
/usr/lib/systemd/system/erp-heat-api.service
/usr/lib/systemd/system/erp-heat-engine.service

%files
/srv/heat/bin
/srv/heat/etc
/srv/heat/include
/srv/heat/lib*
/srv/heat/share
/srv/heat/pip-selfcheck.json
/srv/heat/systemd-services
%attr(-,heat,heat) /var/log/heat
/etc/sudoers.d/heat
/etc/logrotate.d/heat
%attr(-,heat,heat) /etc/heat


%pre
getent group  heat >/dev/null || groupadd -r heat
getent passwd heat >/dev/null || \
    useradd -r -g heat -d /home/heat -s /sbin/nologin \
        -c "OpenStack heat component account" heat
exit 0

%post
for cmd in heat-rootwrap privsep-helper
do
    ln -sf /srv/heat/bin/$cmd /usr/bin/$cmd
done

%post services
for name in api api-cfn engine
do
    systemctl enable erp-heat-$name
done

%changelog
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

* Tue Jan 10 2017 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-build17.15
- Rebuild with CentOS virtualenv tarballs from build #17

* Wed Jan 04 2017 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-build14.14
- Use virtualenv tarballs 14
- Use vnvs build number in release tag

* Thu Dec 15 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-13
- rebuild with CentOS virtualenv build 13

* Fri Dec 09 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-12
- tell sudo that tty is not required

* Fri Dec 09 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-11
- fix ownership for logrotate and sudo config files

* Fri Dec 09 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-10
- set ownership for logs and configs

* Fri Dec 09 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-9
- fix subpackages deps
- added missing log directory

* Fri Dec 09 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-8
- fixing email in changelog

* Fri Dec 09 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-7
- rebuild with centos-virtualenv 11 build

* Thu Dec 08 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-6
- switch to new systemd services

* Tue Dec 06 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-5
- Update to newest virtualenv tarballs built for CentOS

* Mon Dec 05 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-4
- added interpackages dependencies so *-services depend on main one - #2682

* Tue Nov 29 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-3
- *-services requires systemd to be installed for postinstall
- fixed conflict with sudo package

* Mon Nov 28 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-2
- fixed command to enable systemd service
- fixed name of heat-services subpackage

* Wed Nov 16 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-1
- enabled init services
- Handle /etc/heat directory
- handle /usr/local/bin symlinks in post
- added deps from ansible
