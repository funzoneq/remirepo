# Define version and release number
%global version 0.6.0

# Temporarily using git checkout since the release version won't build anymore.
%global release 8.20120613git516bd6f

Name:          php-zmq
Version:       %{version}
Release:       %{release}%{?dist}.1
Summary:       PHP 0MQ/zmq/zeromq extension
# See https://github.com/mkoppanen/php-zmq/pull/58 for discussion
License:       BSD
Group:         Development/Libraries
URL:           http://github.com/mkoppanen/php-zmq
Source:        php-zmq-0.6.0-2.20120613git516bd6f.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: php-devel
BuildRequires: php-cli
%if 0%{?fedora} >= 17 || 0%{?rhel} >= 6
BuildRequires: zeromq3-devel
%else
BuildRequires: zeromq-devel >= 2.0.7
%endif
# needed on EL-5
BuildRequires: pkgconfig

Requires:      php(zend-abi) = %{php_zend_api}
Requires:      php(api) = %{php_core_api}

%{?filter_from_provides: %filter_from_provides /^zmq.so/d}
%{?filter_setup}


%description
PHP extension for the 0MQ/zmq/zeromq messaging system

%prep
%setup -q -c

# duplicate tree for NTS/ZTS build
mv php-zmq nts
cp -pr nts zts


%build
cd nts
%{_bindir}/phpize
%configure  --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

cd ../zts
%{_bindir}/zts-phpize
%configure  --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}


%install
make -C nts install INSTALL_ROOT=%{buildroot}
make -C zts install INSTALL_ROOT=%{buildroot}

# Create the ini location
mkdir -p %{buildroot}/%{php_inidir}
mkdir -p %{buildroot}/%{php_ztsinidir}

# Preliminary extension ini
echo "extension=zmq.so" > %{buildroot}/%{php_inidir}/zmq.ini
echo "extension=zmq.so" > %{buildroot}/%{php_ztsinidir}/zmq.ini


%check
# Minimal load test
%{_bindir}/php     -n -d extension_dir=nts/modules -d extension=zmq.so -m | grep zmq
%{_bindir}/zts-php -n -d extension_dir=zts/modules -d extension=zmq.so -m | grep zmq

cd nts
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
make test


%files
%doc nts/{README,LICENSE}
%defattr(-,root,root,-)
%config(noreplace) %{php_inidir}/zmq.ini
%config(noreplace) %{php_ztsinidir}/zmq.ini
%{php_extdir}/zmq.so
%{php_ztsextdir}/zmq.so


%changelog
* Thu Jan 24 2013 Remi Collet <RPMS@FamilleCollet.com> - 0.6.0-8.20120613git516bd6f
- rebuild

* Mon Nov 05 2012 Ralph Bean <rbean@redhat.com> - 0.6.0-8.20120613git516bd6f
- Add ABI check to conform with PHP guidelines.

* Mon Nov  5 2012 Remi Collet <RPMS@FamilleCollet.com> - 0.6.0-7.20120613git516bd6f
- Rebuilt against zeromq3 when available (fedora >= 17 and RHEL >= 6)
- build ZTS extension

* Mon Oct 22 2012 Ralph Bean <rbean@redhat.com> - 0.6.0-7.20120613git516bd6f
- Rebuilt against zeromq3.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-6.20120613git516bd6f
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 09 2012 Ralph Bean <rbean@redhat.com> - 0.6.0-5.20120613git516bd6f
- Fixed the license field back to just "BSD".  The files thought to be
  PHP-licensed were in fact generated by "phpize" in the %%build section.

* Sat Jun 23 2012 Remi Collet <RPMS@FamilleCollet.com> - 0.6.0-4.20120613git516bd6f
- backport for remi repo

* Thu Jun 14 2012 Ralph Bean <rbean@redhat.com> - 0.6.0-4.20120613git516bd6f
 - Fixed the private-shared-object-provides for reals with John Ciesla's help.
* Wed Jun 13 2012 Ralph Bean <rbean@redhat.com> - 0.6.0-3.20120613git516bd6f
 - Updated License to BSD and PHP.
 - Removed spurious gcc BuildRequires.
 - Fixed private-shared-object-provides.
* Wed Jun 13 2012 Ralph Bean <rbean@redhat.com> - 0.6.0-2.20120613git516bd6f
 - Using tarball of git checkout since the 0.6.0 release won't build anymore.
 - Using valid shortname for BSD license.
 - Added README and LICENSE to the doc
 - Use %%global instead of %%define.
 - Changed 0MQ to 0MQ/zmq/zeromq in Summary and Description to help with
   search.
 - Fully qualified Source URL.
 - Updated to modern BuildRequires.
 - Separated %%build out into %%build and %%install.
 - Removed unnecessary references to buildroot.
 - Removed unnecessary %%defattr.
 - Changed Group from Web/Applications to Development/Libraries.
 - Removed hardcoded Packager tag.
 - Added %%check section.
 - Marked /etc/php.d/zmq.ini as a config file.
* Wed Jun 15 2011 Rick Moran <moran@morangroup.org>
 - Minor Changes.
* Thu Apr 8 2010 Mikko Koppanen <mkoppanen@php.net>
 - Initial spec file
