Name:		erp-neutron
Version:	2016.12
Release:	6%{?dist}
Summary:	OpenStack neutron venv

License:	Apache
Source0:	neutron.tgz
Source1:	neutron.logrotate
Source2:	neutron.sudoers

Requires:	dnsmasq dnsmasq-utils iputils
Requires:	radvd conntrack-tools
Requires:	keepalived ipset iptables psmisc sudo
Requires:	bridge-utils ebtables kmod
Requires(pre):	shadow-utils libvirt

%description

%package services
Summary:	OpenStack neutron venv services
%description services
Requires(post):   systemd
Requires:	erp-neutron

%package compute-node-services
Summary:	OpenStack neutron venv services for compute node
%description compute-node-services
Requires(post):   systemd
Requires:	erp-neutron

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
           %{buildroot}/var/log/neutron \
           %{buildroot}/var/lib/neutron \
           %{buildroot}/usr/local/bin \
           %{buildroot}/etc/logrotate.d \
           %{buildroot}/etc/sudoers.d

install -m 0644 %{_sourcedir}/neutron.logrotate %{buildroot}/etc/logrotate.d/neutron
install -m 0644 %{_sourcedir}/neutron.sudoers   %{buildroot}/etc/sudoers.d/neutron

cp -a * %{buildroot}/srv/neutron/
cp -a src/etc/neutron/* %{buildroot}/etc/neutron/

%files src
/srv/neutron/src

%files
/srv/neutron/bin
/srv/neutron/etc
/srv/neutron/include
/srv/neutron/lib*
/srv/neutron/pip-selfcheck.json
/usr/local/bin
/etc/sudoers.d/neutron
/etc/logrotate.d/neutron
/etc/neutron

%files services
/srv/neutron/neutron-dhcp-agent-init.d
/srv/neutron/neutron-l3-agent-init.d
/srv/neutron/neutron-metadata-agent-init.d
/srv/neutron/neutron-server-init.d

%files compute-node-services
/srv/neutron/neutron-openvswitch-agent-init.d

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
    ln -sf /srv/neutron/bin/$cmd /usr/local/bin/$cmd
done

%post services
for init in dhcp-agent l3-agent metadata-agent server
do
    name=neutron-$init-init.d
    ln -sf /srv/neutron/$name /etc/init.d/$name
    systemctl enable $name
done

%post compute-node-services
for init in openvswitch-agent
do
    name=neutron-$init-init.d
    ln -sf /srv/neutron/$name /etc/init.d/$name
    systemctl enable $name
done

%changelog
* Tue Dec 06 2016 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 2016.12-6
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
