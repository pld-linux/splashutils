#
# TODO
#	- find a way to make it work on startup (not initrd imo, at kernel
#		time - initramfs) + maybe some init.d
#	- check initramfs (upgrade geninitrd maybe), cause splashutils can
#		make use of it
#	- use dietlibc
#
%define		_pre		pre10
%define		_misc_ver	0.1.2
Summary:	Utilities for setting fbsplash
Summary(pl):	Narzêdzia do ustawiania fbsplash
Name:		splashutils
Version:	0.9
Release:	0.%{_pre}.3
License:	GPL
Group:		System
Source0:	http://dev.gentoo.org/~spock/projects/gensplash/current/%{name}-%{version}-%{_pre}.tar.bz2
# Source0-md5:	20ab27ea8e02dc2efb6789cf53663ec8
Source1:	http://dev.gentoo.org/~spock/projects/gensplash/current/miscsplashutils-%{_misc_ver}.tar.bz2
# Source1-md5:	71f85c661c144665ff5d4a8bbef1936e
Source2:	%{name}.init
Source3:	%{name}.sysconfig
Patch0:		%{name}-makefile.patch
URL:		http://dev.gentoo.org/~spock/projects/gensplash/
BuildRequires:	freetype-static
BuildRequires:	glibc-static
BuildRequires:	libjpeg-static
BuildRequires:	libpng-static
BuildRequires:	linux-libc-headers >= 7:2.6.9.1-1.5
BuildRequires:	zlib-static
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Utilities for setting fbsplash.

%description -l pl
Narzêdzia do ustawiania fbsplash.

%prep
%setup -q -n %{name}-%{version}-%{_pre} -a1
find . -name CVS | xargs rm -rf 
%patch0 -p1

rm -rf libs

%build
install -d linux/include
%{__make} splash_kern splash_user
%{__make} -C miscsplashutils-%{_misc_ver} \
	CFLAGS="%{rpmcflags} -I/usr/include/freetype2" \
	LIBDIR="%{_libdir}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/splash,/etc/rc.d/init.d,/etc/sysconfig}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT
install miscsplashutils-%{_misc_ver}/{fbres,fbtruetype/{fbtruetype,fbtruetype.static}} $RPM_BUILD_ROOT%{_bindir}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/fbsplash
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/fbsplash

%clean
rm -rf $RPM_BUILD_ROOT

%post
umask 022 
/sbin/chkconfig --add fbsplash

%preun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del fbsplash
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS README docs/*
%dir %{_sysconfdir}/splash
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) /sbin/*
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/fbsplash
%attr(754,root,root) /etc/rc.d/init.d/fbsplash
