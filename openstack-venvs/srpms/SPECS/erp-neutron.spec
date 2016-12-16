Name:		erp-neutron
Version:	2016.12
Release:	20%{?dist}
Summary:	OpenStack neutron venv

License:	Apache
Source0:	neutron.tgz
Source1:	neutron.logrotate
Source2:	neutron.sudoers

Requires:	dnsmasq dnsmasq-utils iputils
Requires:	radvd conntrack-tools openvswitch
Requires:	keepalived ipset iptables psmisc sudo
Requires:	bridge-utils ebtables kmod
Requires(pre):	shadow-utils libvirt

%description

%package services
Summary:	OpenStack neutron venv services
Requires(post):   systemd
Requires:	erp-neutron
%description services

%package compute-node-services
Summary:	OpenStack neutron venv services for compute node
Requires(post):   systemd
Requires:	erp-neutron
%description compute-node-services

%package src
Summary:	OpenStack neutron venv src
%description src

%prep
%setup -q -n neutron
rm     setup.sh
rm -rf src/.git

%install
install -d \
           %{buildroot}/srv/neutron \
           %{buildroot}/etc/neutron \
           %{buildroot}/usr/lib/systemd/system \
           %{buildroot}/var/log/neutron \
           %{buildroot}/var/lib/neutron \
           %{buildroot}/etc/logrotate.d \
           %{buildroot}/etc/sudoers.d

install -m 0644 %{_sourcedir}/neutron.logrotate %{buildroot}/etc/logrotate.d/neutron
install -m 0644 %{_sourcedir}/neutron.sudoers   %{buildroot}/etc/sudoers.d/neutron

cp -a * %{buildroot}/srv/neutron/
cp -a src/etc/* %{buildroot}/etc/neutron/
mv %{buildroot}/etc/neutron/neutron/* %{buildroot}/etc/neutron/
rm -rf %{buildroot}/etc/neutron/neutron/

cp -a systemd-services/* %{buildroot}/usr/lib/systemd/system/

%files src
/srv/neutron/src

%files
/srv/neutron/bin
/srv/neutron/etc
/srv/neutron/include
/srv/neutron/lib*
/srv/neutron/pip-selfcheck.json
/srv/neutron/systemd-services
%attr(-,neutron,neutron) /var/log/neutron
%attr(-,neutron,neutron) /var/lib/neutron
/etc/sudoers.d/neutron
/etc/logrotate.d/neutron
%attr(-,neutron,neutron) /etc/neutron

%files services
/usr/lib/systemd/system/erp-neutron-server.service

%files compute-node-services
/usr/lib/systemd/system/erp-neutron-openvswitch-agent.service
/usr/lib/systemd/system/erp-neutron-dhcp-agent.service
/usr/lib/systemd/system/erp-neutron-l3-agent.service
/usr/lib/systemd/system/erp-neutron-metadata-agent.service

%pre
getent group  neutron >/dev/null || groupadd -r neutron
getent passwd neutron >/dev/null || \
    useradd -r -g neutron -d /home/neutron -s /sbin/nologin \
        -c "OpenStack neutron component account" neutron
usermod -G libvirt neutron
exit 0

%post
for cmd in neutron-rootwrap privsep-helper neutron-ns-metadata-proxy
do
    ln -sf /srv/neutron/bin/$cmd /usr/bin/$cmd
done

%post services
for name in dhcp-agent l3-agent metadata-agent server
do
    systemctl enable erp-neutron-$name
done

%post compute-node-services
for name in openvswitch-agent
do
    systemctl enable erp-neutron-$name
done

%changelog
* Fri Dec 16 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-20
- move dhcp/l3/metadata agents to compute node services - #2753

* Thu Dec 15 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-19
- added dependency on openvswitch - #2753

* Thu Dec 15 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-18
- rebuild with CentOS virtualenv build 13

* Wed Dec 14 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-17
- ship /var/lib/neutron directory - #2753

* Tue Dec 13 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-16
- erp-neutron: some more /etc/ fixes - #2754

* Mon Dec 12 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-15
- fix handling /etc contents - #2749

* Fri Dec 09 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-14
- tell sudo that tty is not required

* Fri Dec 09 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-13
- fix ownership for logrotate and sudo config files

* Fri Dec 09 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-12
- fixed config files

* Fri Dec 09 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-11
- set ownership for logs and configs

* Fri Dec 09 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-10
- fix subpackages deps
- added missing log directory

* Fri Dec 09 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-9
- fixing email in changelog

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
- enable init services
- provide neutron-ns-metadata-proxy in /usr/local/bin
- move openvswitch-agent init to neutron-compute-node-services
- handle /usr/local/bin symlinks in post
- added deps from ansible
