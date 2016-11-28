Name:		lds-heat
Version:	2016.12
Release:	1%{?dist}
Summary:	OpenStack heat venv

License:	Apache
Source0:	heat.tgz
Source1:	heat.logrotate
Source2:	heat.sudoers

Requires(pre):	shadow-utils

%description

%package heat-services
Summary:	OpenStack heat venv services
%description heat-services

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
           %{buildroot}/var/log/heat \
           %{buildroot}/var/lib/heat/instances \
           %{buildroot}/usr/local/bin \
           %{buildroot}/etc/heat \
           %{buildroot}/etc/logrotate.d \
           %{buildroot}/etc/sudoers.d

install -m 0644 %{_sourcedir}/heat.logrotate %{buildroot}/etc/logrotate.d/heat
install -m 0644 %{_sourcedir}/heat.sudoers   %{buildroot}/etc/sudoers.d/heat

cp -a * %{buildroot}/srv/heat/
cp -a src/etc/heat/* %{buildroot}/etc/heat/

%files src
/srv/heat/src

%files heat-services
/srv/heat/heat-api-cfn-init.d
/srv/heat/heat-api-init.d
/srv/heat/heat-engine-init.d

%files
/srv/heat/bin
/srv/heat/etc
/srv/heat/include
/srv/heat/lib*
/srv/heat/share
/srv/heat/pip-selfcheck.json
/usr/local/bin
/etc


%pre
getent group  heat >/dev/null || groupadd -r heat
getent passwd heat >/dev/null || \
    useradd -r -g heat -d /home/heat -s /sbin/nologin \
        -c "OpenStack heat component account" heat
exit 0

%post
for cmd in heat-rootwrap privsep-helper
do
    ln -sf /srv/heat/bin/$cmd /usr/local/bin/$cmd
done

%post services
for init in api api-cfn engine
do
    name=heat-$init-init.d
    ln -sf /srv/heat/$name /etc/init.d/$name
    systemd enable $name
done

%changelog
* Wed Nov 16 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-1
- enabled init services
- Handle /etc/heat directory
- handle /usr/local/bin symlinks in post
- added deps from ansible
