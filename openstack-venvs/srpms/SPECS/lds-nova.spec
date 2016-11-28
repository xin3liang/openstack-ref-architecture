Name:		lds-nova
Version:	2016.12
Release:	2%{?dist}
Summary:	OpenStack Nova venv

License:	Apache
Source0:	nova.tgz
Source1:	nova.logrotate
Source2:	nova.sudoers

Requires:	libvirt-daemon libvirt-client
Requires:	sysfsutils conntrack ipset
Requires:	python-ceph 
Requires(pre):  shadow-utils libvirt

%description

%package compute-node-services
Summary:	OpenStack Nova venv services for compute node
%description compute-node-services

%package services
Summary:	OpenStack Nova venv services
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
           %{buildroot}/var/log/nova \
           %{buildroot}/var/lib/nova/instances \
           %{buildroot}/usr/local/bin \
           %{buildroot}/etc/logrotate.d \
           %{buildroot}/etc/sudoers.d

install -m 0644 %{_sourcedir}/nova.logrotate %{buildroot}/etc/logrotate.d/nova
install -m 0644 %{_sourcedir}/nova.sudoers   %{buildroot}/etc/sudoers.d/nova

cp -a * %{buildroot}/srv/nova/
cp -a src/etc/nova/* %{buildroot}/etc/nova/

%files src
/srv/nova/src

%files compute-node-services
/srv/nova/nova-compute-init.d

%files services
/srv/nova/nova-api-init.d
/srv/nova/nova-cert-init.d
/srv/nova/nova-conductor-init.d
/srv/nova/nova-consoleauth-init.d
/srv/nova/nova-scheduler-init.d

%files
/srv/nova/bin
/srv/nova/etc
/srv/nova/include
/srv/nova/lib*
/srv/nova/share
/srv/nova/pip-selfcheck.json
/usr/local/bin
/etc/sudoers.d/nova
/etc/logrotate.d/nova
/etc/nova


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
    ln -sf /srv/nova/bin/$cmd /usr/local/bin/$cmd
done

%post services
for init in api cert conductor consoleauth scheduler
do
    name=nova-$init-init.d
    ln -sf /srv/nova/$name /etc/init.d/$name
    systemctl enable $name
done

%post compute-node-services
for init in compute
do
    name=nova-$init-init.d
    ln -sf /srv/nova/$name /etc/init.d/$name
    systemctl enable $name
done

%changelog
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
