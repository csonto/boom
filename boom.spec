%global with_python2 1
%global with_python3 1
%ifnarch s390x s390
%global with_grub2 1
%else
%global with_grub2 0
%endif
%global boolean_dependencies 1

%global summary A set of libraries and tools for managing boot loader entries

# TODO: There is a dead boom package in Fedora (up to 25), we may need:
# - another name for top level package (boom-boot suggested)
# - add Conflict:
Name: boom
Version: 0.8.2.fedora.1
Release: 1%{?dist}
Summary: %{summary}

License: GPLv2
URL: https://github.com/bmr-cymru/boom
# My repo for package review only:
Source0: https://github.com/csonto/boom/archive/%{version}/%{name}-%{version}.tar.gz
# Upstream:
#Source0: https://github.com/bmr-cymru/boom/archive/%{version}/%{name}-%{version}.tar.gz

BuildArch: noarch
%if 0%{?with_python2}
BuildRequires: python2-devel
BuildRequires: python2-setuptools
%endif
%if 0%{?with_python3}
BuildRequires: python3-devel
BuildRequires: python3-setuptools
%endif

%description
Boom is a boot manager for Linux systems using boot loaders that support
the BootLoader Specification for boot entry configuration.

Boom requires a BLS compatible boot loader to function: either the
systemd-boot project, or Grub2 with the bls patch (Red Hat Grub2 builds
include this support in both Red Hat Enterprise Linux 7 and Fedora).

%if 0%{?with_python2}
%package -n python2-boom
Summary: %{summary}
%{?python_provide:%python_provide python2-boom}
%if 0%{?boolean_dependencies}
Requires: (boom-grub2 if grub2)
Recommends: (lvm2 or btrfs-progs)
%endif

%description -n python2-boom
Boom is a boot manager for Linux systems using boot loaders that support
the BootLoader Specification for boot entry configuration.

Boom requires a BLS compatible boot loader to function: either the
systemd-boot project, or Grub2 with the bls patch (Red Hat Grub2 builds
include this support in both Red Hat Enterprise Linux 7 and Fedora).

This package provides the python2 version of boom.
%endif # with_python2

%if 0%{?with_python3}
%package -n python3-boom
Summary: %{summary}
%{?python_provide:%python_provide python3-boom}
%if 0%{?boolean_dependencies}
Requires: (boom-grub2 if grub2)
Recommends: (lvm2 or btrfs-progs)
%endif

%description -n python3-boom
Boom is a boot manager for Linux systems using boot loaders that support
the BootLoader Specification for boot entry configuration.

Boom requires a BLS compatible boot loader to function: either the
systemd-boot project, or Grub2 with the bls patch (Red Hat Grub2 builds
include this support in both Red Hat Enterprise Linux 7 and Fedora).

This package provides the python3 version of boom.
%endif # with_python3

%if 0%{?with_grub2}
%package -n boom-grub2
Summary: %{summary}
Requires: grub2

%description -n boom-grub2
Boom is a boot manager for Linux systems using boot loaders that support
the BootLoader Specification for boot entry configuration.

Boom requires a BLS compatible boot loader to function: either the
systemd-boot project, or Grub2 with the bls patch (Red Hat Grub2 builds
include this support in both Red Hat Enterprise Linux 7 and Fedora).

This package provides integration scripts for grub2 bootloader.
%endif # with_grub2

%prep
%autosetup -n boom-%{version}

%build
%if 0%{?with_python2}
%py2_build
%endif
%if 0%{?with_python3}
%py3_build
%endif

%install
%if 0%{?with_python2}
%py2_install
%endif
%if 0%{?with_python3}
%py3_install
%endif

# Install Grub2 integration scripts
install -d -m 700 ${RPM_BUILD_ROOT}/etc/grub.d
install -d -m 755 ${RPM_BUILD_ROOT}/etc/default
install -m 755 etc/grub.d/42_boom ${RPM_BUILD_ROOT}/etc/grub.d
install -m 644 etc/default/boom ${RPM_BUILD_ROOT}/etc/default

# Make configuration directories
install -d -m 700 ${RPM_BUILD_ROOT}/boot/boom/profiles
install -d -m 700 ${RPM_BUILD_ROOT}/boot/loader/entries
install -m 644 examples/profiles/*.profile ${RPM_BUILD_ROOT}/boot/boom/profiles

install -d -m 755 ${RPM_BUILD_ROOT}/%{_mandir}/man8
install -m 644 man/man8/boom.8 ${RPM_BUILD_ROOT}/%{_mandir}/man8

%check
%if 0%{?with_python2}
%{__python2} setup.py test
%endif
%if 0%{?with_python3}
%{__python3} setup.py test
%endif

%if 0%{?with_python2}
%files -n python2-boom
%license COPYING
%doc README.md
%if !0%{?with_python3}
%{_bindir}/boom
%doc %{_mandir}/man8/boom.*
%endif
%{python2_sitelib}/*
%doc examples/
%doc tests/
/boot/*
%endif # with_python2

%if 0%{?with_python3}
%files -n python3-boom
%license COPYING
%doc README.md
%{python3_sitelib}/*
%{_bindir}/boom
%doc %{_mandir}/man8/boom.*
%doc examples/
%doc tests/
/boot/*
%endif # with_python3

%if 0%{?with_grub2}
%files -n boom-grub2
/etc/default/boom
/etc/grub.d/42_boom
%endif # with_grub2

%changelog
* Tue Feb 06 2018 Marian Csontos <mcsontos@redhat.com> = 0.8.2.fedora.1-1
- New upstream bugfix release
- boom script uses python3 by default
- Split grub2 support into subpackage

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
