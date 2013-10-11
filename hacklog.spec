%if ! (0%{?rhel} >= 6 || 0%{?fedora} > 12)
%global with_python26 1
%define pybasever 2.6
%define __python_ver 26
%define __python %{_bindir}/python%{?pybasever}
%endif

%global include_tests 1

%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%{!?pythonpath: %global pythonpath %(%{__python} -c "import os, sys; print(os.pathsep.join(sys.path))")}

Name: hacklog
Version: 0.0.1
Release: 1%{?dist}
Summary: Hacklog Server

Group:   System Environment/Daemons
License: GPLv3
URL:     https://github.com/dandb/hacklog/
Source0: https://github.com/dandb/%{name}/archive/%{name}-%{version}.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch: noarch

Requires: python-sqlalchemy
Requires: python-twisted

%if 0%{?with_python26}
BuildRequires: python26-twisted
BuildRequires: python26-sqlalchemy
BuildRequires: python26-setuptools

Requires: python26-twisted
Requires: python26-sqlalchemy

%else

%if ((0%{?rhel} >= 6 || 0%{?fedora} > 12) && 0%{?include_tests})
BuildRequires: python-sqlalchemy
BuildRequires: python-twisted
BuildRequires: python-setuptools
%endif


%if ! (0%{?rhel} >= 7 || 0%{?fedora} >= 15)
Requires(post): chkconfig
Requires(preun): chkconfig
Requires(preun): initscripts
Requires(postun): initscripts

%else
%if 0%{?systemd_preun:1}

Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

%endif

%endif

%endif

%description
Hacklog is a system daemon that that detect compromised user accounts
by applying statical analysis to auth,authpriv log events.
It was created by "Hacking Outliers" project during Q4 2013
hackweek at Dun & Bradstreet Credibility Corp.


%prep
%setup -c
#%setup -T -D -a 1

%build

%install
rm -rf $RPM_BUILD_ROOT
cd $RPM_BUILD_DIR/%{name}-%{version}/%{name}-%{version}
%{__python} setup.py install -O1 --root $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/
mkdir -p $RPM_BUILD_ROOT%{_bindir}
install -p -m 0640 conf/server.conf $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/server.conf
install -p -m 0755 bin/%{name} $RPM_BUILD_ROOT%{_bindir}/%{name}
install -p -m 0755 scripts/%{name}.init.d $RPM_BUILD_ROOT%{_initrddir}/%{name}

%if ((0%{?rhel} >= 6 || 0%{?fedora} > 12) && 0%{?include_tests})
%check
cd $RPM_BUILD_DIR/%{name}-%{version}/%{name}-%{version}
PYTHONPATH=%{pythonpath}:$RPM_BUILD_DIR/%{name}-%{version}/%{name}-%{version} %{__python} setup.py test --runtests-opts=-u
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc $RPM_BUILD_DIR/%{name}-%{version}/%{name}-%{version}/README.md
%doc $RPM_BUILD_DIR/%{name}-%{version}/%{name}-%{version}/CHANGES
%doc $RPM_BUILD_DIR/%{name}-%{version}/%{name}-%{version}/LICENSE
%{python_sitelib}/%{name}/*
%{python_sitelib}/%{name}-%{version}-py?.?.egg-info

%files -n hacklog
%defattr(-,root,root)
%{_bindir}/%{name}
%if ! (0%{?rhel} >= 7 || 0%{?fedora} >= 15)
%attr(0755, root, root) %{_initrddir}/%{name}
%else
%{_unitdir}/%{name}.service
%endif
%config(noreplace) %{_sysconfdir}/hacklog/server.conf

# less than RHEL 8 / Fedora 16
# not sure if RHEL 7 will use systemd yet
%if ! (0%{?rhel} >= 7 || 0%{?fedora} >= 15)

%preun -n hacklog
  if [ $1 -eq 0 ] ; then
      /sbin/service hacklog stop >/dev/null 2>&1
      /sbin/chkconfig --del hacklog
  fi

%post -n hacklog
  /sbin/chkconfig --add hacklog

%postun -n hacklog
  if [ "$1" -ge "1" ] ; then
      /sbin/service hacklog restart >/dev/null 2>&1 || :

  fi

%endif

%changelog
* Thu Oct 10 2013 Konstantin Antselovich <kantselovich@dandb.com> - 0.1.0-1
- First version of hacklog spec file 0.1.0
