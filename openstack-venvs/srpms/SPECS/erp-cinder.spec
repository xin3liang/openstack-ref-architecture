Name:		erp-cinder
Version:	2016.12
Release:	16%{?dist}
Summary:	OpenStack cinder venv

License:	Apache
Source0:	cinder.tgz
Source1:	cinder.logrotate
Source2:	cinder.sudoers

Requires:	ceph-common python-ceph sysfsutils
Requires:	lvm2 sudo qemu-img
Requires:	python-rados python-rbd
Requires(pre):  shadow-utils

%description

%package services
Summary:	OpenStack cinder venv services
Requires(post):   systemd
Requires:	erp-cinder
%description services

%package compute-node-services
Summary:	OpenStack cinder venv services for compute node
Requires(post):   systemd
Requires:	erp-cinder
%description compute-node-services

%package src
Summary:	OpenStack cinder venv src
%description src

%prep
%setup -q -n cinder
rm     setup.sh
rm -rf src/.git

%install
install -d \
           %{buildroot}/srv/cinder \
           %{buildroot}/etc/cinder \
           %{buildroot}/usr/lib/systemd/system \
           %{buildroot}/var/log/cinder \
           %{buildroot}/var/lib/cinder \
           %{buildroot}/etc/logrotate.d \
           %{buildroot}/etc/sudoers.d

install -m 0644 %{_sourcedir}/cinder.logrotate %{buildroot}/etc/logrotate.d/cinder
install -m 0644 %{_sourcedir}/cinder.sudoers   %{buildroot}/etc/sudoers.d/cinder

cp -a * %{buildroot}/srv/cinder/
cp -a src/etc/cinder/* %{buildroot}/etc/cinder/
cp -a systemd-services/* %{buildroot}/usr/lib/systemd/system/

%files src
/srv/cinder/src

%files
/srv/cinder/bin
/srv/cinder/etc
/srv/cinder/include
/srv/cinder/lib*
/srv/cinder/share
/srv/cinder/pip-selfcheck.json
/srv/cinder/systemd-services
%attr(-,cinder,cinder) /var/log/cinder
%attr(-,cinder,cinder) /var/lib/cinder
/etc/sudoers.d/cinder
/etc/logrotate.d/cinder
%attr(-,cinder,cinder) /etc/cinder

%files services
/usr/lib/systemd/system/erp-cinder-api.service
/usr/lib/systemd/system/erp-cinder-scheduler.service

%files compute-node-services
/usr/lib/systemd/system/erp-cinder-volume.service

%pre
getent group  cinder >/dev/null || groupadd -r cinder
getent passwd cinder >/dev/null || \
    useradd -r -g cinder -d /home/cinder -s /sbin/nologin \
        -c "OpenStack cinder component account" cinder
exit 0

%post
for cmd in cinder-rootwrap privsep-helper
do
    ln -sf /srv/cinder/bin/$cmd /usr/bin/$cmd
done

%post services
for name in api scheduler
do
    systemctl enable erp-cinder-$name
done

%post compute-node-services
for name in volume
do
    systemctl enable erp-cinder-$name
done

%changelog
* Tue Dec 13 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-16
- erp-cinder: ship /var/lib/cinder - #2752

* Mon Dec 12 2016 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 2016.12-15
- cinder user do not have to be in libvirt group - #2751

* Fri Dec 09 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-14
- tell sudo that tty is not required

* Fri Dec 09 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-13
- fix ownership for logrotate and sudo config files

* Fri Dec 09 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-12
- set ownership for logs and configs

* Fri Dec 09 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-11
- fix subpackages deps
- added missing log directory

* Fri Dec 09 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-10
- fixing email in changelog

* Fri Dec 09 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-9
- added missing deps on python-rados, python-rdb

* Fri Dec 09 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-8
- rebuild with centos-virtualenv 11 build

* Thu Dec 08 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-7
- switch to new systemd services

* Tue Dec 06 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-6
- Update to newest virtualenv tarballs built for CentOS

* Mon Dec 05 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-5
- added interpackages dependencies so *-services depend on main one - #2682

* Tue Nov 29 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-4
- added more dependencies

* Tue Nov 29 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-3
- *-services requires systemd to be installed for postinstall

* Mon Nov 28 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-2
- fixed conflict with sudo package
- fixed command to enable systemd service
- predepend on libvirt to have it's group when we create user

* Wed Nov 16 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-1
- enabled init services
- handle /etc/cinder
- create /usr/local/bin/ symlinks in post to not conflict with glance
- move compute node services into separate package
