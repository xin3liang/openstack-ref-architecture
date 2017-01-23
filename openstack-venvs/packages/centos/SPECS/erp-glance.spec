Name:		erp-glance
Version:	2016.12.build24
Release:	5%{?dist}
Summary:	OpenStack glance venv

License:	Apache
Source0:	glance.tgz
Source1:	glance.logrotate
Source2:	glance.sudoers

Requires:	python-ceph
Requires:	python-rados python-rbd
Requires(pre):	shadow-utils libvirt

%description

%package services
Summary:	OpenStack glance venv services
Requires(post):   systemd
Requires:	erp-glance
%description services

%package src
Summary:	OpenStack glance venv src
%description src

%prep
%setup -q -n glance
rm     setup.sh
rm -rf src/.git

%install
install -d \
           %{buildroot}/srv/glance \
           %{buildroot}/etc/glance \
           %{buildroot}/usr/lib/systemd/system \
           %{buildroot}/var/log/glance \
           %{buildroot}/var/lib/glance \
           %{buildroot}/etc/logrotate.d \
           %{buildroot}/etc/sudoers.d

install -m 0644 %{_sourcedir}/glance.logrotate %{buildroot}/etc/logrotate.d/glance
install -m 0644 %{_sourcedir}/glance.sudoers   %{buildroot}/etc/sudoers.d/glance

cp -a * %{buildroot}/srv/glance/
cp -a src/etc/* %{buildroot}/etc/glance/
cp -a systemd-services/* %{buildroot}/usr/lib/systemd/system/

%files src
/srv/glance/src

%files
/srv/glance/bin
/srv/glance/etc
/srv/glance/include
/srv/glance/lib*
/srv/glance/share
/srv/glance/pip-selfcheck.json
/srv/glance/systemd-services
%attr(-,glance,glance) /var/log/glance
/etc/sudoers.d/glance
/etc/logrotate.d/glance
%attr(-,glance,glance) /etc/glance

%files services
/usr/lib/systemd/system/erp-glance-api.service
/usr/lib/systemd/system/erp-glance-registry.service

%pre
getent group  glance >/dev/null || groupadd -r glance
getent passwd glance >/dev/null || \
    useradd -r -g glance -d /home/glance -s /sbin/nologin \
        -c "OpenStack glance component account" glance
usermod -G libvirt glance
exit 0

%post
for cmd in glance-rootwrap privsep-helper
do
    ln -sf /srv/glance/bin/$cmd /usr/bin/$cmd
done

%post services
for name in api registry
do
    systemctl enable erp-glance-$name
done

%changelog
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

* Tue Jan 10 2017 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-build17.16
- Rebuild with CentOS virtualenv tarballs from build #17

* Wed Jan 04 2017 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-build14.15
- Use virtualenv tarballs 14
- Use vnvs build number in release tag

* Thu Dec 15 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-14
- rebuild with CentOS virtualenv build 13

* Fri Dec 09 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-13
- tell sudo that tty is not required

* Fri Dec 09 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-12
- fix ownership for logrotate and sudo config files

* Fri Dec 09 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-11
- set ownership for logs and configs

* Fri Dec 09 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-10
- fix subpackages deps
- added missing log directory

* Fri Dec 09 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-9
- fixing email in changelog

* Fri Dec 09 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-8
- added missing deps on python-rados, python-rdb

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

* Mon Nov 28 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-2
- fixed conflict with sudo package
- fixed command to enable systemd service

* Wed Nov 16 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-1
- enable init services
- dropped libvirt-qemu group
- handle /etc/glance directory
- added deps from ansible
- create /usr/local/bin/ symlinks in post to not conflict with cinder
