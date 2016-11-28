Name:		lds-cinder
Version:	2016.12
Release:	1%{?dist}
Summary:	OpenStack cinder venv

License:	Apache
Source0:	cinder.tgz
Source1:	cinder.logrotate
Source2:	cinder.sudoers

Requires:	ceph-common python-ceph sysfsutils
Requires(pre):  shadow-utils

%description

%package services
Summary:	OpenStack cinder venv services
%description services

%package compute-node-services
Summary:	OpenStack cinder venv services for compute node
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
           %{buildroot}/var/log/cinder \
           %{buildroot}/var/lib/cinder \
           %{buildroot}/usr/local/bin \
           %{buildroot}/etc/logrotate.d \
           %{buildroot}/etc/sudoers.d

install -m 0644 %{_sourcedir}/cinder.logrotate %{buildroot}/etc/logrotate.d/cinder
install -m 0644 %{_sourcedir}/cinder.sudoers   %{buildroot}/etc/sudoers.d/cinder

cp -a * %{buildroot}/srv/cinder/
cp -a src/etc/cinder/* %{buildroot}/etc/cinder/

%files src
/srv/cinder/src

%files
/srv/cinder/bin
/srv/cinder/etc
/srv/cinder/include
/srv/cinder/lib*
/srv/cinder/share
/srv/cinder/pip-selfcheck.json
/etc

%files services
/srv/cinder/cinder-api-init.d
/srv/cinder/cinder-scheduler-init.d

%files compute-node-services
/srv/cinder/cinder-volume-init.d

%pre
getent group  cinder >/dev/null || groupadd -r cinder
getent passwd cinder >/dev/null || \
    useradd -r -g cinder -d /home/cinder -s /sbin/nologin \
        -c "OpenStack cinder component account" cinder
usermod -G libvirt cinder
exit 0

%post
for cmd in cinder-rootwrap privsep-helper
do
    ln -sf /srv/cinder/bin/$cmd /usr/local/bin/$cmd
done

%post services
for init in api scheduler
do
    name=cinder-$init-init.d
    ln -sf /srv/cinder/$name /etc/init.d/$name
    systemd enable $name
done

%post compute-node-services
for init in volume
do
    name=cinder-$init-init.d
    ln -sf /srv/cinder/$name /etc/init.d/$name
    systemd enable $name
done

%changelog
* Wed Nov 16 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-0.9
- enabled init services
- handle /etc/cinder
- create /usr/local/bin/ symlinks in post to not conflict with lds-glance
- move compute node services into separate package
