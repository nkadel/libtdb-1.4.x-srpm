%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif
%{!?python_version: %global python_version %(%{__python} -c "from distutils.sysconfig import get_python_version; print(get_python_version())")}

Name: libtdb
Version: 1.2.11
Release: 1%{?dist}
Group: System Environment/Daemons
Summary: The tdb library
License: LGPLv3+
URL: http://tdb.samba.org/
Source: http://samba.org/ftp/tdb/tdb-%{version}.tar.gz
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires: autoconf
BuildRequires: libxslt
BuildRequires: docbook-style-xsl
BuildRequires: python-devel

Provides: bundled(libreplace)

# Patches

%description
A library that implements a trivial database.

%package devel
Group: Development/Libraries
Summary: Header files need to link the Tdb library
Requires: libtdb = %{version}-%{release}
Requires: pkgconfig

%description devel
Header files needed to develop programs that link against the Tdb library.

%package -n tdb-tools
Group: Development/Libraries
Summary: Developer tools for the Tdb library
Requires: libtdb = %{version}-%{release}

%description -n tdb-tools
Tools to manage Tdb files

%package -n python-tdb
Group: Development/Libraries
Summary: Python bindings for the Tdb library
Requires: libtdb = %{version}-%{release}

%description -n python-tdb
Python bindings for libtdb

%prep
%setup -q -n tdb-%{version}

%build
%configure --disable-rpath \
           --bundled-libraries=NONE \
           --builtin-libraries=replace
make %{?_smp_mflags} V=1

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# Shared libraries need to be marked executable for
# rpmbuild to strip them and include them in debuginfo
find $RPM_BUILD_ROOT -name "*.so*" -exec chmod -c +x {} \;

rm -f $RPM_BUILD_ROOT%{_libdir}/libtdb.a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_libdir}/libtdb.so.*

%files devel
%defattr(-,root,root)
%doc docs/README
%{_includedir}/tdb.h
%{_libdir}/libtdb.so
%{_libdir}/pkgconfig/tdb.pc

%files -n tdb-tools
%defattr(-,root,root,-)
%{_bindir}/tdbbackup
%{_bindir}/tdbdump
%{_bindir}/tdbtool
%{_bindir}/tdbrestore
%{_mandir}/man8/tdbbackup.8*
%{_mandir}/man8/tdbdump.8*
%{_mandir}/man8/tdbtool.8*
%{_mandir}/man8/tdbrestore.8*

%files -n python-tdb
%defattr(-,root,root,-)
%{python_sitearch}/tdb.so

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post -n python-tdb -p /sbin/ldconfig

%postun -n python-tdb -p /sbin/ldconfig

%changelog
* Sun Dec 01 2012 Jakub Hrozek <jhrozek@redhat.com> - 1.2.11-1
- New upstream release 1.2.11

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.10-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 22 2012 Stephen Gallagher <sgallagh@redhat.com> - 1.2.10-15
- New upstream release 1.2.10
- Remove upstreamed patches
- Provides functionality for the upcoming Samba 4 beta

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.9-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 01 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.2.9-13
- Add patch to ignore --disable-silent-rules
- Include README documentation

* Wed Nov 23 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.2.9-12
- Add explicit mention of the bundled libreplace
- https://fedorahosted.org/fpc/ticket/120


* Wed Nov 09 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.2.9-11
- Rebuild for F17 due to bz#744766

* Tue Apr  5 2011 Simo Sorce <ssorce@redhat.com> - 1.2.9-9
- Add patch to limit database expansion, was causing OOMs in SSSD in some
  extreme situations.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.9-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 14 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.2.9-8
- Actually fix the verbosity

* Fri Jan 14 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.2.9-7
- Let rpmbuild strip binaries, make build more verbose.
- Original patch by Ville SkyttÃ¤ <ville.skytta@iki.fi>

* Wed Jan 12 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.2.9-6
- Install python bindings into the correct location

* Tue Jan 11 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.2.9-5
- Run ldconfig on python-tdb

* Tue Jan 11 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.2.9-4
- Do not delete a necessary file during %%install

* Tue Jan 11 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.2.9-3
- Bump release to rebuild with the correct sources in place

* Tue Jan 11 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.2.9-2
- Bump build to rebuild with sources in place

* Tue Jan 11 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.2.9-1
- New upstream bugfix release
- Adds a new tdbrestore utility
- Convert to new WAF build-system
- Add python bindings in new python-tdb subpackage

* Wed Feb 24 2010 Simo Sorce <ssorce@redhat.com> - 1.2.1-3
- add missing build require

* Wed Feb 24 2010 Simo Sorce <ssorce@redhat.com> - 1.2.1-2
- Fix spec file
- Package manpages too

* Wed Feb 24 2010 Simo Sorce <ssorce@redhat.com> - 1.2.1-1
- New upstream bugfix release

* Tue Dec 15 2009 Simo Sorce <ssorce@redhat.com> - 1.2.0-1
- New upstream release

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 17 2009 Simo Sorce <ssorce@redhat.com> - 1.1.5-1
- Original tarballs had a screw-up, rebuild with new fixed tarballs from
  upstream.

* Tue Jun 16 2009 Simo Sorce <ssorce@redhat.com> - 1.1.5-0
- New upstream release

* Wed May 6 2009 Simo Sorce <ssorce@redhat.com> - 1.1.3-15
- First public independent release from upstream
