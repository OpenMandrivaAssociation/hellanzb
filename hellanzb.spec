Name:           hellanzb
Version:        0.13
Release:        %mkrel 4
Summary:        Hands-free nzb downloader and post processor

Group:          Networking/News
License:        BSD
URL:            http://www.hellanzb.com/trac/
Source0:        http://www.hellanzb.com/distfiles/hellanzb-%{version}.tar.gz
Source1:        README.urpmi
Patch0:         hellanzb-configuration-location3.patch
Patch1:         hellanzb-unrar-is-optional.patch
Patch2:         hellanzb-remove-bogus-shebang.patch
Patch3:         hellanzb-0.13-dont-attempt-multiple-groups.diff
# (ahmad) add patch from debian to fix compatibility with Twisted 10.0.0
# http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=573221
Patch4:         007-Twisted_10.0.0_compat.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:  python-devel
BuildRequires:  python-setuptools
BuildArch:      noarch

Requires:       parchive2
Requires:       python-twisted
Requires:       python-twisted-web
Requires:       python-yenc


%description
hellanzb is an easy to use application designed to retrieve nzb files
and fully process them. The goal being to make getting files from Usenet
as hands-free as possible. Once fully installed, all that's required
is moving an nzb file to the queue directory. The rest: downloading,
par-checking, un-raring, etc. is done automatically by hellanzb.


%prep
%setup -q
%patch0
sed --in-place 's|\*DOCDIR\*|%{_docdir}|' Hellanzb/Core.py
sed --in-place 's|\*PKGNAME\*|%{name}|'   Hellanzb/Core.py
%patch1
%patch2
%patch3
%patch4 -p1 -b .twisted 


%build
%{__python} -c 'import setuptools; execfile("setup.py")' build


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_sysconfdir}
%{__python} -c 'import setuptools; execfile("setup.py")' install --skip-build --root %{buildroot}

mv %{buildroot}%{_bindir}/%{name}.py %{buildroot}%{_bindir}/%{name}
rm %{buildroot}/usr/etc/%{name}.conf.sample

mv etc/hellanzb.conf.sample %{buildroot}/%{_docdir}/%{name}/
cp %{SOURCE1} %{buildroot}%{_docdir}/%{name}/

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_docdir}/%{name}/
%{python_sitelib}/*
%{_bindir}/%{name}
