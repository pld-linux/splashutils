#
# TODO
#	- find a way to make it work on startup (not initrd imo, at kernel
#		time - initramfs) + maybe some init.d
#	- check initramfs (upgrade geninitrd maybe), cause splashutils can
#		make use of it
#	- update dirs in scripts
#
Summary:	Utilities for setting fbsplash
Summary(pl.UTF-8):	Narzędzia do ustawiania fbsplash
Name:		splashutils
Version:	1.3
Release:	2
License:	GPL
Group:		Applications/System
Source0:	http://dev.gentoo.org/~spock/projects/gensplash/archive/%{name}-%{version}.tar.bz2
# Source0-md5:	c7c92b98e34b860511aa57bd29d62f76
%define		_misc_ver	0.1.5
Source1:	http://dev.gentoo.org/~spock/projects/gensplash/current/misc%{name}-%{_misc_ver}.tar.bz2
# Source1-md5:	20fc3ed2407edc8cd97623bf7f1c5c7b
Source2:	%{name}.init
Source3:	%{name}.sysconfig
Patch0:		%{name}-makefile.patch
Patch1:		%{name}-compile.patch
Patch2:		%{name}-pld-paths.patch
Patch3:		%{name}-no-dereference.patch
URL:		http://dev.gentoo.org/~spock/projects/gensplash/
BuildRequires:	freetype-static
BuildRequires:	glibc-static
BuildRequires:	klibc-static >= 1.1.1-1
BuildRequires:	libjpeg-static
BuildRequires:	libpng-static
BuildRequires:	linux-libc-headers >= 7:2.6.9.1-1.5
BuildRequires:	zlib-static
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
Suggests:	fbsplash-theme
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Utilities for setting fbsplash.

%description -l pl.UTF-8
Narzędzia do ustawiania fbsplash.

%prep
%setup -q -a1
%patch0 -p0
%patch1 -p0
%patch2 -p1
%patch3 -p1

%build
./configure \
	--with-fbsplash \
	--with-fifo=/var/run/splashutils/.splash \
	--with-png \
	--with-themedir=%{_sysconfdir}/splash \
	--with-ttf \
	--with-ttfkern

%{__make} objdir

%{__make} splash_kern \
	CC="%{__cc}"

%{__make} splash_user \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -Os"

%{__make} -C miscsplashutils-%{_misc_ver} \
	CFLAGS="%{rpmcflags} -Os -I/usr/include/freetype2" \
	LIBDIR="%{_libdir}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/splash,/etc/rc.d/init.d,/etc/sysconfig} \
	    $RPM_BUILD_ROOT/var/run/%{name}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT
install miscsplashutils-%{_misc_ver}/{fbres,fbtruetype/{fbtruetype,fbtruetype.static}} $RPM_BUILD_ROOT%{_bindir}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/fbsplash
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/fbsplash

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add fbsplash

%preun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del fbsplash
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS README docs/*
%dir %{_sysconfdir}/splash
%dir %attr(755,root,root) /var/run/splashutils
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) /sbin/*
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/fbsplash
%attr(754,root,root) /etc/rc.d/init.d/fbsplash
