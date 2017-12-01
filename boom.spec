%if 0%{?rhel}
%global py2_pkgname python-boom
%else
%global py2_pkgname python2-boom
%global with_python3 1
%global sphinx_docs 1
%endif

%global summary A set of libraries and tools for managing boot loader entries

%global commit 8d23c42902dc3f3d48f981797814c4dcf4a0f273
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name: boom	
Version: 0.8.1
Release: 0.1.20171201git%{shortcommit}%{?dist}
Summary: %{summary}

Group: Applications/System
License: GPLv2
URL: https://github.com/bmr-cymru/boom	
#Source0: boom-%%{version}.tar.gz
#Source0: https://github.com/csonto/boom/archive/v%%{version}.tar.gz
Source0: https://github.com/csonto/boom/archive/%{commit}/%{name}-%{shortcommit}.tar.gz

BuildArch: noarch

BuildRequires: python2-devel
%if 0%{!?with_python3:1}
BuildRequires: python-setuptools
%endif

%if 0%{?with_python3}
BuildRequires: python2-setuptools
#BuildRequires: python2-sphinx
BuildRequires: python3-devel
BuildRequires: python3-sphinx
BuildRequires: python3-setuptools
%endif # if with_python3

%description
Boom is a boot manager for Linux systems using boot loaders that support
the BootLoader Specification for boot entry configuration.

Boom requires a BLS compatible boot loader to function: either the
systemd-boot project, or Grub2 with the bls patch (Red Hat Grub2 builds
include this support in both Red Hat Enterprise Linux 7 and Fedora).

%package -n %{?py2_pkgname}
Summary: %{summary}
%{?python_provide:%python_provide python2-boom}

%description -n %{?py2_pkgname}
Boom is a boot manager for Linux systems using boot loaders that support
the BootLoader Specification for boot entry configuration.

Boom requires a BLS compatible boot loader to function: either the
systemd-boot project, or Grub2 with the bls patch (Red Hat Grub2 builds
include this support in both Red Hat Enterprise Linux 7 and Fedora).

This package provides the python2 version of boom.


%if 0%{?with_python3}
%package -n python3-boom
Summary: %{summary}
%{?python_provide:%python_provide python3-boom}

%description -n python3-boom
Boom is a boot manager for Linux systems using boot loaders that support
the BootLoader Specification for boot entry configuration.

Boom requires a BLS compatible boot loader to function: either the
systemd-boot project, or Grub2 with the bls patch (Red Hat Grub2 builds
include this support in both Red Hat Enterprise Linux 7 and Fedora).

This package provides the python3 version of boom.


%endif # if with_python3
%prep
#%%autosetup -n boom-%%{version}
%autosetup -n boom-%{commit}

%build
%py2_build

%if 0%{?with_python3}
%py3_build
%endif # if with_python3

%install
# Install Python3 first, so that the py2 build of usr/bin/boom is not
# overwritten by the py3 version of the script.
%if 0%{?with_python3}
# NOTE: This will not build and install doc on el7
%py3_install
make -C doc html BUILDDIR=../doc
%endif # if with_python3

%py2_install

# Install Grub2 integration scripts
mkdir -p ${RPM_BUILD_ROOT}/etc/grub.d
mkdir -p ${RPM_BUILD_ROOT}/etc/default
install -m 755 etc/grub.d/42_boom ${RPM_BUILD_ROOT}/etc/grub.d
install -m 644 etc/default/boom ${RPM_BUILD_ROOT}/etc/default

# Make configuration directories
mkdir -p ${RPM_BUILD_ROOT}/boot/boom/profiles
mkdir -p ${RPM_BUILD_ROOT}/boot/loader/entries
install -d -m 750 ${RPM_BUILD_ROOT}/boot/boom/profiles ${RPM_BUILD_ROOT}
install -d -m 750 ${RPM_BUILD_ROOT}/boot/loader/entries ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}/%{_mandir}/man8
install -m 644 man/man8/boom.8 ${RPM_BUILD_ROOT}/%{_mandir}/man8

%check
%{__python2} setup.py test

%if 0%{?with_python3}
%{__python3} setup.py test
%endif # if with_python3

%files -n %{?py2_pkgname}
%license COPYING
%doc README.md
%doc %{_mandir}/man8/boom.*
%if 0%{?sphinx_docs}
%doc doc/html/
%endif # if sphinx_docs
%doc examples/*
%{python2_sitelib}/*
%{_bindir}/boom
/etc/grub.d/42_boom
%config(noreplace) /etc/default/boom
/boot/*

%if 0%{?with_python3}
%files -n python3-boom
%license COPYING
%doc README.md
%doc %{_mandir}/man8/boom.*
%if 0%{?sphinx_docs}
%doc doc/html/
%endif # if sphinx_docs
%doc examples/*
%{python3_sitelib}/*
/etc/grub.d/42_boom
/etc/default/boom
/boot/*
%endif # if with_python3

%changelog
* Fri Dec 01 2017 Marian Csontos <mcsontos@redhat.com> 0.8.1-0.1.20171201git8d23c429
- Test upstream packaging

* Tue Oct 31 2017 Bryn M. Reeves <bmr@redhat.com> = 0.8-1
- Merge spec file changes from mcsontos
- Add boom.8 manual page
- Update minor version number

* Fri Oct 27 2017 Bryn M. Reeves <bmr@redhat.com> = 0.1-4
- Update RPM build to latest master

* Sat Oct 21 2017 Bryn M. Reeves <bmr@redhat.com> = 0.1-2
- Prevent py3 boom script clobbering py2 version

* Thu Oct 19 2017 Bryn M. Reeves <bmr@redhat.com> = 0.1-1
- Initial RPM spec
