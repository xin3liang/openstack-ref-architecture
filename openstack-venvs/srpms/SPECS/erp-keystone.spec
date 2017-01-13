Name:		erp-keystone
Version:	2016.12.build20
Release:	2%{?dist}
Summary:	OpenStack keystone venv

License:	Apache
Source0:	keystone.tgz

Requires:	httpd mod_wsgi MySQL-python
Requires(pre):  shadow-utils

%description

%package src
Summary:	OpenStack keystone venv src
%description src

%prep
%setup -q -n keystone
rm     setup.sh
rm -rf src/.git

%install
install -d \
           %{buildroot}/srv/keystone \
           %{buildroot}/etc/keystone

cp -a * %{buildroot}/srv/keystone/
cp -a src/etc/* %{buildroot}/etc/keystone/
rm -f %{buildroot}/srv/keystone/apache.conf

%files src
/srv/keystone/src

%files
/srv/keystone/bin
/srv/keystone/etc
/srv/keystone/include
/srv/keystone/lib*
/srv/keystone/pip-selfcheck.json
/etc/keystone

%pre
getent group  keystone >/dev/null || groupadd -r keystone
getent passwd keystone >/dev/null || \
    useradd -r -g keystone -d /home/keystone -s /sbin/nologin \
        -c "OpenStack keystone component account" keystone
exit 0

%changelog
* Fri Jan 13 2017 root - 2016.12.build20-2
- Rebuild with CentOS virtualenv tarballs from build #20

* Wed Jan 11 2017 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12.build19-1
- Rebuild with CentOS venv build #19

* Tue Jan 10 2017 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-build17.10
- Rebuild with CentOS virtualenv tarballs from build #17

* Wed Jan 04 2017 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-build14.9
- Use virtualenv tarballs 14
- Use vnvs build number in release tag

* Thu Dec 15 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-8
- rebuild with CentOS virtualenv build 13

* Fri Dec 09 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-7
- create keystone user

* Fri Dec 09 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-6
- fixing email in changelog

* Fri Dec 09 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-5
- rebuild with centos-virtualenv 11 build

* Tue Dec 06 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-4
- Update to newest virtualenv tarballs built for CentOS

* Mon Dec 05 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-3
- removed apache config - #2687

* Mon Nov 28 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-2
- changed list of files to not own whole /etc

* Tue Nov 15 2016 Marcin Juszkiewicz <marcin.juszkiewicz@linaro.org> - 2016.12-1
- handle /etc/keystone directory
- added deps from ansible
