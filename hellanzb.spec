Name:           hellanzb
Version:        0.13
Release:        %mkrel 1
Summary:        Hands-free nzb downloader and post processor

Group:          Networking/News
License:        BSD
URL:            http://www.hellanzb.com/trac/
Source0:        http://www.hellanzb.com/distfiles/hellanzb-%{version}.tar.gz
Source1:        README.Mandriva
Patch0:         hellanzb-configuration-location3.patch
Patch1:         hellanzb-unrar-is-optional.patch
Patch2:         hellanzb-remove-bogus-shebang.patch
Patch3:         hellanzb-0.13-dont-attempt-multiple-groups.diff
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


%build
%{__python} -c 'import setuptools; execfile("setup.py")' build


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}
%{__python} -c 'import setuptools; execfile("setup.py")' install --skip-build --root $RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT/%{_bindir}/%{name}.py $RPM_BUILD_ROOT/%{_bindir}/%{name}
rm $RPM_BUILD_ROOT/usr/etc/%{name}.conf.sample

mv etc/hellanzb.conf.sample $RPM_BUILD_ROOT/%{_docdir}/%{name}/
cp %{SOURCE1} $RPM_BUILD_ROOT/%{_docdir}/%{name}/README.Fedora


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_docdir}/%{name}/
%{py_platsitedir}/*
%{_bindir}/%{name}
