#
# TODO
#	- find a way to make it work on startup (not initrd imo, at kernel
#		time - initramfs) + maybe some init.d
#	- check initramfs (upgrade geninitrd maybe), cause splashutils can
#		make use of it
#
Summary:	Utilities for setting fbsplash
Summary(pl):	Narzêdzia do ustawiania fbsplash
Name:		splashutils
Version:	1.1.9.10
Release:	0.3
License:	GPL
Group:		System
Source0:	http://dev.gentoo.org/~spock/projects/gensplash/archive/%{name}-%{version}.tar.bz2
# Source0-md5:	af1230e0f1bda32b519a6accf6ade734
%define		_misc_ver	0.1.3
Source1:	http://dev.gentoo.org/~spock/projects/gensplash/current/miscsplashutils-%{_misc_ver}.tar.bz2
# Source1-md5:	f8e92992682bbaf8e6eb2316ac708bc0
Source2:	%{name}.init
Source3:	%{name}.sysconfig
Patch0:		%{name}-makefile.patch
Patch1:		%{name}-config.patch
URL:		http://dev.gentoo.org/~spock/projects/gensplash/
BuildRequires:	freetype-static
BuildRequires:	glibc-static
BuildRequires:	klibc-static >= 1.1.1-1
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
%setup -q -a1
%patch0 -p1
%patch1 -p1
rm -rf libs/klibc*
rm -rf libs/zlib*

%build
%{__make} splash_kern \
	CC=klcc

%{__make} splash_user \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -Os"

%{__make} -C miscsplashutils-%{_misc_ver} \
	CFLAGS="%{rpmcflags} -Os -I/usr/include/freetype2" \
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
