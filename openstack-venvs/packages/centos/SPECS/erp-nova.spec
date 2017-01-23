Name:		erp-nova
Version:	2016.12.build24
Release:	5%{?dist}
Summary:	OpenStack Nova venv

License:	Apache
Source0:	nova.tgz
Source1:	nova.logrotate
Source2:	nova.sudoers

Requires:	bridge-utils
Requires:	conntrack
Requires:	conntrack-tools
Requires:	curl
Requires:	dnsmasq
Requires:	dnsmasq-utils
Requires:	ebtables
Requires:	genisoimage
Requires:	ipmitool
Requires:	ipset
Requires:	iptables iptables-ipv6
Requires:	iscsi-initiator-utils
Requires:	libvirt-client
Requires:	libvirt-daemon-kvm
Requires:	libvirt-python
Requires:	lvm2
Requires:	openssh
Requires:	openssh-clients
Requires:	python-ceph
Requires:	python-libguestfs
Requires:	qemu-system-aarch64
Requires:	radvd
Requires:	rsync
Requires:	sg3_utils
Requires:	sudo
Requires:	sysfsutils

Requires(pre):  shadow-utils libvirt

%description

%package compute-node-services
Summary:	OpenStack Nova venv services for compute node
Requires(post):   systemd
Requires:	erp-nova
%description compute-node-services

%package services
Summary:	OpenStack Nova venv services
Requires(post):   systemd
Requires:	erp-nova
%description services

%package src
Summary:	OpenStack Nova venv src
%description src

%prep
%setup -q -n nova
rm     setup.sh
rm -rf src/.git

%install
install -d \
           %{buildroot}/srv/nova \
           %{buildroot}/etc/nova \
           %{buildroot}/usr/lib/systemd/system \
           %{buildroot}/var/log/nova \
           %{buildroot}/var/lib/nova/instances \
           %{buildroot}/etc/logrotate.d \
           %{buildroot}/etc/sudoers.d

install -m 0644 %{_sourcedir}/nova.logrotate %{buildroot}/etc/logrotate.d/nova
install -m 0644 %{_sourcedir}/nova.sudoers   %{buildroot}/etc/sudoers.d/nova

cp -a * %{buildroot}/srv/nova/
cp -a src/etc/nova/* %{buildroot}/etc/nova/
cp -a systemd-services/* %{buildroot}/usr/lib/systemd/system/



%files src
/srv/nova/src

%files compute-node-services
/usr/lib/systemd/system/erp-nova-compute.service

%files services
/usr/lib/systemd/system/erp-nova-api.service
/usr/lib/systemd/system/erp-nova-cert.service
/usr/lib/systemd/system/erp-nova-conductor.service
/usr/lib/systemd/system/erp-nova-consoleauth.service
/usr/lib/systemd/system/erp-nova-scheduler.service

%files
/srv/nova/bin
/srv/nova/etc
/srv/nova/include
/srv/nova/lib*
/srv/nova/share
/srv/nova/pip-selfcheck.json
/srv/nova/systemd-services
%attr(-,nova,nova) /var/lib/nova
%attr(-,nova,nova) /var/log/nova
/etc/sudoers.d/nova
/etc/logrotate.d/nova
%attr(-,nova,nova) /etc/nova


%pre
getent group  nova >/dev/null || groupadd -r nova
getent passwd nova >/dev/null || \
    useradd -r -g nova -d /home/nova -s /sbin/nologin \
        -c "OpenStack nova component account" nova
usermod -G libvirt nova
exit 0

%post
for cmd in nova-rootwrap privsep-helper
do
    ln -sf /srv/nova/bin/$cmd /usr/bin/$cmd
done

%post services
for name in api cert conductor consoleauth scheduler
do
    systemctl enable erp-nova-$name
done

%post compute-node-services
for name in compute
do
    systemctl enable erp-nova-$name
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

* Mon Dec 12 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-13
- ship /var/lib/nova - #2746

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
- added set of missing dependencies
- *-services requires systemd to be installed for postinstall

* Mon Nov 28 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-2
- fixed conflict with sudo package
- fixed command to enable systemd service
- predepend on libvirt to have it's group when we create user

* Wed Nov 16 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-1
- enabled init services
- handle /usr/local/bin symlinks in postinstall
- handle /etc/nova directory
- added deps from ansible
- move compute node services into separate package
