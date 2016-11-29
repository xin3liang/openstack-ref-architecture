Name:		lds-glance
Version:	2016.12
Release:	3%{?dist}
Summary:	OpenStack glance venv

License:	Apache
Source0:	glance.tgz
Source1:	glance.logrotate
Source2:	glance.sudoers

Requires:	python-ceph
Requires(pre):	shadow-utils libvirt

%description

%package services
Summary:	OpenStack glance venv services
%description services
Requires(post):   systemd

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
           %{buildroot}/var/log/glance \
           %{buildroot}/var/lib/glance \
           %{buildroot}/usr/local/bin \
           %{buildroot}/etc/logrotate.d \
           %{buildroot}/etc/sudoers.d

install -m 0644 %{_sourcedir}/glance.logrotate %{buildroot}/etc/logrotate.d/glance
install -m 0644 %{_sourcedir}/glance.sudoers   %{buildroot}/etc/sudoers.d/glance

cp -a * %{buildroot}/srv/glance/
cp -a src/etc/* %{buildroot}/etc/glance/

%files src
/srv/glance/src

%files
/srv/glance/bin
/srv/glance/etc
/srv/glance/include
/srv/glance/lib*
/srv/glance/share
/srv/glance/pip-selfcheck.json
/etc/sudoers.d/glance
/etc/logrotate.d/glance
/etc/glance

%files services
/srv/glance/glance-api-init.d
/srv/glance/glance-registry-init.d

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
    ln -sf /srv/glance/bin/$cmd /usr/local/bin/$cmd
done

%post services
for init in api registry
do
    name=glance-$init-init.d
    ln -sf /srv/glance/$name /etc/init.d/$name
    systemctl enable $name
done

%changelog
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
- create /usr/local/bin/ symlinks in post to not conflict with lds-cinder
